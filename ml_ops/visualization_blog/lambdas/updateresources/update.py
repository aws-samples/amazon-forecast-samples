from os import environ
import codecs
import csv
import re
from datetime import datetime
from io import StringIO
from boto3 import client, resource
from schemas import SCHEMAS_DEF
from pyathena import connect

S3_CLI = client('s3')
S3 = resource('s3')


def get_type_string(forecast_type):
    try:
        return 'p{:.0f}'.format(float(forecast_type) * 100)
    except ValueError:
        return forecast_type


# Move an object within the specified bucket.
def move_object(bucket, source, destination):
    S3_CLI.copy_object(
        Bucket=bucket,
        CopySource='{bucket}/{key}'.format(bucket=bucket, key=source),
        Key=destination
    )
    S3_CLI.delete_object(Bucket=bucket, Key=source)


# Standardize output from Amazon Forecast, adding type field.
def get_readings(params, bucket):
    def create_table(table_name, attributes, input_path, delimiter=','):
        for attribute in attributes:
            if attribute['AttributeName'] == 'timestamp':
                attribute['AttributeType'] = 'string'
        properties = ', '.join(
            [
                '{} {}'.format(field['AttributeName'], field['AttributeType'])
                for field in attributes
            ]
        )

        # Update table schema if it exists
        cursor.execute('DROP TABLE IF EXISTS {};'.format(table_name))
        cursor.execute(
            '''
            CREATE EXTERNAL TABLE IF NOT EXISTS {table} ({properties})
            ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
            WITH SERDEPROPERTIES (
                'serialization.format' = ',',
                'field.delim' = '{delimiter}')
            LOCATION '{input_path}'
            TBLPROPERTIES ('has_encrypted_data'='false','skip.header.line.count'='1');
            '''.format(
                table=table_name,
                properties=properties,
                delimiter=delimiter,
                input_path=input_path
            )
        )

    cursor = connect(
        s3_staging_dir='s3://{}/stage/ '.format(bucket),
        region_name=environ['AWS_REGION'],
        work_group=environ['ATHENA_WORKGROUP']
    ).cursor()
    identifier = SCHEMAS_DEF[params['DatasetGroup']['Domain']]['identifier']
    datetimestr = '%Y-%m-%d' if params['TimestampFormat'
                                      ] == 'yyyy-MM-dd' else '%Y-%m-%d %H:%i:%s'

    create_table(
        table_name='train',
        attributes=params['Datasets'][0]['Schema']['Attributes'],
        input_path='s3://{}/train/'.format(bucket)
    )

    create_table(
        table_name='forecast',
        attributes=params['Datasets'][0]['Schema']['Attributes'] +
        [{
            'AttributeName': 'type',
            'AttributeType': 'string'
        }],
        input_path='s3://{}/quicksight/'.format(bucket)
    )

    cursor.execute(
        '''
            select * from (
                select {identifier}, max(date_parse(timestamp, '{date_format}')) as date from train
                group by {identifier}
            ) as x
            INNER JOIN train AS t
            ON t.{identifier} = x.{identifier}
            AND x.date = date_parse(t.timestamp, '{date_format}')
        '''.format(identifier=identifier, date_format=datetimestr)
    )

    attributes = params['Datasets'][0]['Schema']['Attributes']

    for row in cursor:
        query_field = list(row[-len(attributes):])
        for forecast_type in params['Forecast']['ForecastTypes']:
            yield {
                **{
                    attributes[i]['AttributeName']: query_field[i]
                    for i in range(len(attributes))
                },
                **{
                    'type': get_type_string(forecast_type)
                }
            }


def transform(s3_object, bucket, key, params, page):
    # Transform forecast output into input format
    csv_buffer = StringIO()
    schema = SCHEMAS_DEF[params['Datasets'][0]['Domain']]
    fieldnames = [
        attr['AttributeName']
        for attr in params['Datasets'][0]['Schema']['Attributes']
    ]
    out = csv.DictWriter(csv_buffer, fieldnames=fieldnames + ['type'])
    out.writeheader()
    stream = codecs.getreader('utf-8')(s3_object.get()['Body'])
    datetimestr = '%Y-%m-%d' if params['TimestampFormat'
                                      ] == 'yyyy-MM-dd' else '%Y-%m-%d %H:%M:%S'
    for row in csv.DictReader(stream):
        row[schema['date']
           ] = datetime.strptime(row.pop('date'),
                                 '%Y-%m-%dT%H:%M:%SZ').strftime(datetimestr)
        for forecast_type in params['Forecast']['ForecastTypes']:
            row['type'] = 'p{:.0f}'.format(float(forecast_type) * 100)
            row[schema['metric']] = row.pop(get_type_string(forecast_type))
            out.writerow(
                {field: row[field]
                 for field in schema['fields'] + ['type']}
            )

    if page == 0:
        for entry in get_readings(params, bucket):
            out.writerow(entry)

    S3_CLI.put_object(Body=csv_buffer.getvalue(), Bucket=bucket, Key=key)


def lambda_handler(event, context):
    outdated_objects = S3_CLI.list_objects_v2(
        Bucket=event['bucket'], Prefix='quicksight'
    )
    new_objects = S3_CLI.list_objects_v2(Bucket=event['bucket'], Prefix='tmp/')
    bucket = S3.Bucket(event['bucket'])
    if 'Contents' in outdated_objects.keys():
        for key in [obj['Key'] for obj in outdated_objects['Contents']]:
            move_object(
                bucket=event['bucket'],
                source=key,
                destination='history/clean/{}'.format(key.split('/')[1])
            )
    if 'Contents' in new_objects.keys():
        for page, key in enumerate([obj['Key'] for obj in new_objects['Contents']]):
            if re.match('^.*\.(csv|CSV)', key):
                transform(
                    bucket.Object(key=key),
                    bucket=event['bucket'],
                    key='format_{}'.format(key),
                    params=event['params'],
                    page=page
                )
                move_object(
                    bucket=event['bucket'],
                    source='format_{}'.format(key),
                    destination='quicksight/{}'.format(key.split('/')[1])
                )
                move_object(
                    bucket=event['bucket'],
                    source=key,
                    destination='history/raw/{}'.format(key.split('/')[1])
                )

    return event

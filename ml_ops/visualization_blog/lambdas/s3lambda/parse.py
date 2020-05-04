import os
from json import loads, dumps
from datetime import datetime
from boto3 import client
# from jsonschema import validate
from schema import SCHEMA_DEF

STEP_FUNCTIONS_CLI = client('stepfunctions')


def get_params(bucket_name, key_name):
    params = loads(
        client('s3').get_object(Bucket=bucket_name,
                                Key=key_name)['Body'].read().decode('utf-8')
    )
    # validate(params, SCHEMA_DEF)
    return params


def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    return dumps(
        STEP_FUNCTIONS_CLI.start_execution(
            stateMachineArn=os.environ['STEP_FUNCTIONS_ARN'],
            name=datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
            input=dumps(
                {
                    'bucket': bucket_name,
                    'currentDate': datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
                    'params':
                        get_params(bucket_name, os.environ['PARAMS_FILE'])
                }
            )
        ),
        default=str
    )

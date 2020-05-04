from os import environ
from boto3 import client
import actions
from loader import Loader

ACCOUNTID = client('sts').get_caller_identity()['Account']
ARN = 'arn:aws:forecast:{region}:{account}:dataset/{name}'
LOADER = Loader()


def lambda_handler(event, context):
    datasets = event['params']['Datasets']
    status = None
    event['DatasetArn'] = ARN.format(
        account=ACCOUNTID,
        name=datasets[0]['DatasetName'],
        region=environ['AWS_REGION']
    )
    event['AccountID'] = ACCOUNTID
    try:
        status = LOADER.forecast_cli.describe_dataset(
            DatasetArn=event['DatasetArn']
        )
    except LOADER.forecast_cli.exceptions.ResourceNotFoundException:
        LOADER.logger.info('Dataset not found! Will follow to create dataset.')
        for dataset in datasets:
            LOADER.forecast_cli.create_dataset(**dataset)
        status = LOADER.forecast_cli.describe_dataset(
            DatasetArn=event['DatasetArn']
        )

    actions.take_action(status['Status'])
    return event

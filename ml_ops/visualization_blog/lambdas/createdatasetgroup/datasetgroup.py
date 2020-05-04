from os import environ
import actions
from loader import Loader

ARN = 'arn:aws:forecast:{region}:{account}:dataset-group/{name}'
LOADER = Loader()


def lambda_handler(event, context):
    dataset_group = event['params']['DatasetGroup']
    status = None
    event['DatasetGroupArn'] = ARN.format(
        account=event['AccountID'],
        name=dataset_group['DatasetGroupName'],
        region=environ['AWS_REGION']
    )
    try:
        status = LOADER.forecast_cli.describe_dataset_group(
            DatasetGroupArn=event['DatasetGroupArn']
        )

    except LOADER.forecast_cli.exceptions.ResourceNotFoundException:
        LOADER.logger.info(
            'Dataset Group not found! Will follow to create Dataset Group.'
        )
        LOADER.forecast_cli.create_dataset_group(
            **dataset_group, DatasetArns=[event['DatasetArn']]
        )
        status = LOADER.forecast_cli.describe_dataset_group(
            DatasetGroupArn=event['DatasetGroupArn']
        )

    actions.take_action(status['Status'])
    return event

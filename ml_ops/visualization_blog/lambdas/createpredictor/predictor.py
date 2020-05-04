from os import environ
import actions
from loader import Loader

ARN = 'arn:aws:forecast:{region}:{account}:predictor/{name}'
LOADER = Loader()


def lambda_handler(event, context):
    status = None
    predictor = event['params']['Predictor']
    event['PredictorArn'] = ARN.format(
        account=event['AccountID'],
        date=event['currentDate'],
        name=predictor['PredictorName'],
        region=environ['AWS_REGION']
    )
    try:
        status = LOADER.forecast_cli.describe_predictor(
            PredictorArn=event['PredictorArn']
        )

    except LOADER.forecast_cli.exceptions.ResourceNotFoundException:
        LOADER.logger.info(
            'Predictor not found! Will follow to create new predictor.'
        )
        if 'InputDataConfig' in predictor.keys():
            predictor['InputDataConfig']['DatasetGroupArn'] = event[
                'DatasetGroupArn']
        else:
            predictor['InputDataConfig'] = {
                'DatasetGroupArn': event['DatasetGroupArn']
            }
        LOADER.forecast_cli.create_predictor(**predictor)
        status = LOADER.forecast_cli.describe_predictor(
            PredictorArn=event["PredictorArn"]
        )
    actions.take_action(status['Status'])
    return event

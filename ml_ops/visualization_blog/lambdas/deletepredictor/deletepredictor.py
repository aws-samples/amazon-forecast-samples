import actions
from loader import Loader

LOADER = Loader()


def lambda_handler(event, context):
    try:
        LOADER.forecast_cli.delete_predictor(PredictorArn=event['PredictorArn'])
        actions.take_action_delete(
            LOADER.forecast_cli.describe_predictor(
                PredictorArn=event['PredictorArn']
            )['Status']
        )

    except (LOADER.forecast_cli.exceptions.ResourceNotFoundException, KeyError):
        LOADER.logger.info('Predictor not found! Passing.')

    return event

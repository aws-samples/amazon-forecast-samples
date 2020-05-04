import actions
from loader import Loader

LOADER = Loader()


def lambda_handler(event, context):
    # Delete forecast export job
    try:
        LOADER.forecast_cli.delete_forecast_export_job(
            ForecastExportJobArn=event['ExportJobArn']
        )
        actions.take_action_delete(
            status=LOADER.forecast_cli.describe_forecast_export_job(
                ForecastExportJobArn=event['ExportJobArn']
            )['Status']
        )
    except (LOADER.forecast_cli.exceptions.ResourceNotFoundException, KeyError):
        LOADER.logger.info('Forecast export job not found. Passing.')

    # Delete forecast
    try:
        LOADER.forecast_cli.delete_forecast(ForecastArn=event['ForecastArn'])
        actions.take_action_delete(
            LOADER.forecast_cli.describe_forecast(
                ForecastArn=event['ForecastArn']
            )['Status']
        )
    except (LOADER.forecast_cli.exceptions.ResourceNotFoundException, KeyError):
        LOADER.logger.info('Forecast not found. Passing.')

    return event

import actions
from loader import Loader

LOADER = Loader()


def lambda_handler(event, context):
    try:
        LOADER.forecast_cli.delete_dataset_import_job(
            DatasetImportJobArn=event['DatasetImportJobArn']
        )
        actions.take_action_delete(
            LOADER.forecast_cli.describe_dataset_import_job(
                DatasetImportJobArn=event['DatasetImportJobArn']
            )['Status']
        )

    except (LOADER.forecast_cli.exceptions.ResourceNotFoundException, KeyError):
        LOADER.logger.info('Import job not found! Passing.')

    return event

import time
import boto3
import json
import pandas as pd
import logging
import matplotlib.pyplot as plt

def wait_till_delete(callback, check_time = 5, timeout = 180):
    elapsed_time = 0
    while elapsed_time < timeout:
        try:
            out = callback()
        except Exception as e:
            # When given the resource not found exception, deletion has occured
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logging.info('Successful delete\n')
                return
            # Fails with other error
            logging.info(f'Deletion failed: {e}')
            return(e)
        time.sleep(check_time)  # units of seconds
        elapsed_time += check_time

def wait(callback, time_interval=30):
    last_status = callback()['Status']
    time.sleep(time_interval)
    elapsed_time = time_interval
    is_failed = True

    while (last_status != 'ACTIVE'):
        last_status = callback()['Status']
        time.sleep(time_interval)  # units of seconds
        elapsed_time += time_interval
        print('.', end='', flush=True)
        if last_status == 'CREATE_FAILED':
            break
    if last_status == "ACTIVE":
        is_failed = False
    job_status = "failed" if is_failed else "success"
    print('')
    logging.info(f"Finished in {elapsed_time} seconds with status {job_status}")
    return not is_failed

def load_exact_sol(fname, item_id, is_schema_perm=False):
    exact = pd.read_csv(fname, header = None)
    exact.columns = ['item_id', 'timestamp', 'target']
    if is_schema_perm:
        exact.columns = ['timestamp', 'target', 'item_id']
    return exact.loc[exact['item_id'] == item_id]

def get_or_create_role_arn():
    iam = boto3.client("iam")
    role_name = "ForecastRoleDemo"
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
              "Effect": "Allow",
              "Principal": {
                "Service": "forecast.amazonaws.com"
              },
              "Action": "sts:AssumeRole"
            }
        ]
    }
    role_arn = None
    try:
        create_role_response = iam.create_role(
            RoleName = role_name,
            AssumeRolePolicyDocument = json.dumps(assume_role_policy_document)
        )
        role_arn = create_role_response["Role"]["Arn"]
    except iam.exceptions.EntityAlreadyExistsException:
        print("The role " + role_name + "exists, ignore to create it")
        role_arn = boto3.resource('iam').Role(role_name).arn
    policy_arn = "arn:aws:iam::aws:policy/AmazonForecastFullAccess"
    iam.attach_role_policy(
        RoleName = role_name,
        PolicyArn = policy_arn
    )
    iam.attach_role_policy(
        PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess',
        RoleName=role_name
    )
    time.sleep(60) # wait for a minute to allow IAM role policy attachment to propagate
    print(role_arn)
    return role_arn


def plot_forecasts(fcsts, exact, freq = '1H', forecastHorizon=24, time_back = 80):
    p10 = pd.DataFrame(fcsts['Forecast']['Predictions']['p10'])
    p50 = pd.DataFrame(fcsts['Forecast']['Predictions']['p50'])
    p90 = pd.DataFrame(fcsts['Forecast']['Predictions']['p90'])
    pred_int = p50['Timestamp'].apply(lambda x: pd.Timestamp(x))
    fcst_start_date = pred_int[0]
    time_int = exact['timestamp'].apply(lambda x: pd.Timestamp(x))
    plt.plot(time_int[-time_back:],exact['target'].values[-time_back:], color = 'r')
    plt.plot(pred_int, p50['Value'].values, color = 'k');
    plt.fill_between(p50['Timestamp'].values, 
                     p10['Value'].values,
                     p90['Value'].values,
                     color='b', alpha=0.3);
    plt.axvline(x=pd.Timestamp(fcst_start_date), linewidth=3, color='g', ls='dashed');
    plt.axvline(x=pd.Timestamp(fcst_start_date, freq)+forecastHorizon-1, linewidth=3, color='g', ls='dashed');
    plt.xticks(rotation=30);
    plt.legend(['Target', 'Forecast'], loc = 'lower left')
    

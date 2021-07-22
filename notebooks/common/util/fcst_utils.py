import re
import io
import time
import json
import gzip

import boto3
import botocore.exceptions

import pandas as pd
import matplotlib.pyplot as plt

import util.notebook_utils


def wait_till_delete(callback, check_time = 5, timeout = None):

    elapsed_time = 0
    while timeout is None or elapsed_time < timeout:
        try:
            out = callback()
        except botocore.exceptions.ClientError as e:
            # When given the resource not found exception, deletion has occured
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print('Successful delete')
                return
            else:
                raise
        time.sleep(check_time)  # units of seconds
        elapsed_time += check_time

    raise TimeoutError( "Forecast resource deletion timed-out." )


def wait(callback, time_interval = 10):

    status_indicator = util.notebook_utils.StatusIndicator()

    while True:
        status = callback()['Status']
        status_indicator.update(status)
        if status in ('ACTIVE', 'CREATE_FAILED'): break
        time.sleep(time_interval)

    status_indicator.end()
    
    return (status=="ACTIVE")


def load_exact_sol(fname, item_id, is_schema_perm=False):
    exact = pd.read_csv(fname, header = None)
    exact.columns = ['item_id', 'timestamp', 'target']
    if is_schema_perm:
        exact.columns = ['timestamp', 'target', 'item_id']
    return exact.loc[exact['item_id'] == item_id]


def get_or_create_iam_role( role_name ):

    iam = boto3.client("iam")

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

    try:
        create_role_response = iam.create_role(
            RoleName = role_name,
            AssumeRolePolicyDocument = json.dumps(assume_role_policy_document)
        )
        role_arn = create_role_response["Role"]["Arn"]
        print("Created", role_arn)
        
        print("Attaching policies...")
        iam.attach_role_policy(
            RoleName = role_name,
            PolicyArn = "arn:aws:iam::aws:policy/AmazonForecastFullAccess"
        )

        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess',
        )

        print("Waiting for a minute to allow IAM role policy attachment to propagate")
        time.sleep(60)
    except iam.exceptions.EntityAlreadyExistsException:
        print("The role " + role_name + " exists, ignore to create it")
        role_arn = boto3.resource('iam').Role(role_name).arn

    print("Done.")
    return role_arn


def delete_iam_role( role_name ):
    iam = boto3.client("iam")
    iam.detach_role_policy( PolicyArn = "arn:aws:iam::aws:policy/AmazonS3FullAccess", RoleName = role_name )
    iam.detach_role_policy( PolicyArn = "arn:aws:iam::aws:policy/AmazonForecastFullAccess", RoleName = role_name )
    iam.delete_role(RoleName=role_name)


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region
    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).
    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        elif region == "us-east-1":
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except Exception as e:
        print(e)
        return False
    return True


def empty_s3_path( s3_client, s3_path ):

    if s3_path[-1] != "/":
        s3_path += "/"

    # extract s3 bucket and s3 key
    re_result = re.match( "s3://([^/]+)/(.*)", s3_path )
    if re_result:
        bucket_name = re_result.group(1)
        prefix = re_result.group(2)
    else:
        raise ValueError( "S3 path format error", src )

    cont_token = None
    while True:
        list_param = {
            "Bucket" : bucket_name, 
            "Prefix" : prefix,
        }
        if cont_token:
            list_param["ContinuationToken"] = cont_token
        
        response = s3_client.list_objects_v2( **list_param )
        
        delete_param = {
            "Bucket" : bucket_name, 
            "Delete" : {
                "Objects" : []
            },
        }
        
        if "Contents" in response:
            for item in response["Contents"]:
                if item["Key"].endswith("/") : continue
                
                print(item["Key"])
                
                delete_param["Delete"]["Objects"].append(
                    {
                        "Key" : item["Key"]
                    }
                )
                
            s3_client.delete_objects( **delete_param )

        if "NextContinuationToken" in response:
            cont_token = response["NextContinuationToken"]
            continue
        
        break

        
def read_exported_forecast_into_dataframe( s3_client, s3_path ):

    if s3_path[-1] != "/":
        s3_path += "/"

    # extract s3 bucket and s3 key
    re_result = re.match( "s3://([^/]+)/(.*)", s3_path )
    if re_result:
        bucket_name = re_result.group(1)
        prefix = re_result.group(2)
    else:
        raise ValueError( "S3 path format error", src )

    s3_objects = []
    cont_tolen = None
    
    # list objects
    while True:
        params = { "Bucket" : bucket_name, "Prefix" : prefix }
        if cont_tolen:
            params["ContinuationToken"] = cont_tolen
    
        response = s3_client.list_objects_v2( **params )
        s3_objects += response["Contents"]
        
        if "NextContinuationToken" not in response:
            break

        cont_tolen = response["NextContinuationToken"]
    
    df_list = []
    
    # read objects and convert to pandas dataframes
    for obj in s3_objects:
        key = obj["Key"]
        
        if not key.endswith(".csv"):
            continue
        
        print(key)

        fd = io.BytesIO()
        s3_client.download_fileobj( Bucket=bucket_name, Key=key, Fileobj=fd )
        fd.seek(0)
        
        df_part = pd.read_csv(fd)
        df_list.append(df_part)
    
    df = pd.concat( df_list )
    
    df["date"] = pd.to_datetime( df["date"], format="%Y-%m-%dT%H:%M:00Z" )
    
    return df


def plot_forecasts(fcsts, exact, freq = '1H', forecastHorizon=24, time_back = 80):
    p10 = pd.DataFrame(fcsts['Forecast']['Predictions']['p10'])
    p50 = pd.DataFrame(fcsts['Forecast']['Predictions']['p50'])
    p90 = pd.DataFrame(fcsts['Forecast']['Predictions']['p90'])
    pred_int = p50['Timestamp'].apply(lambda x: pd.Timestamp(x))
    fcst_start_date = pred_int.iloc[0]
    fcst_end_date = pred_int.iloc[-1]
    time_int = exact['timestamp'].apply(lambda x: pd.Timestamp(x))
    plt.plot(time_int[-time_back:],exact['target'].values[-time_back:], color = 'r')
    plt.plot(pred_int, p50['Value'].values, color = 'k')
    plt.fill_between(pred_int, 
                     p10['Value'].values,
                     p90['Value'].values,
                     color='b', alpha=0.3);
    plt.axvline(x=pd.Timestamp(fcst_start_date), linewidth=3, color='g', ls='dashed')
    plt.axvline(x=pd.Timestamp(fcst_end_date), linewidth=3, color='g', ls='dashed')
    plt.xticks(rotation=30)
    plt.legend(['Target', 'Forecast'], loc = 'lower left')


def extract_gz( src, dst ):
    
    print( f"Extracting {src} to {dst}" )    

    with open(dst, 'wb') as fd_dst:
        with gzip.GzipFile( src, 'rb') as fd_src:
            data = fd_src.read()
            fd_dst.write(data)

    print("Done.")


#!/usr/bin/env python3

"""
The script sets up the role for Forecast to assume in the customer whitelisted
account. The user running the script should have some basic AWS permissions. An
example of a light weight policy is provided here:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "forecast:*"
                "s3:*",
                "iam:GetRole",
                "iam:GetUser",
                "iam:ListRoles",
                "iam:ListUsers",
                "iam:ListGroups",
                "iam:CreateRole",
                "iam:PutRolePolicy",
                "iam:PutUserPolicy",
                "iam:UpdateAssumeRolePolicy",
                "kms:List*",
                "kms:Get*",
                "kms:Describe*",
                "kms:Create*"
            ],
            "Resource": "*"
        }
    ]
}

Run python setup_forecast_permissions.py <bucket_name> to get started
"""

import boto3
import json
import logging
import sys
import time
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
import argparse

ROLE_NAME = 'amazonforecast'
FORECAST_ADMIN_POLICY_ARN = 'arn:aws:iam::aws:policy/service-role/AmazonForecastFullAccess'
SERVICE_PRINCIPAL_DICT = {
    'prod': 'forecast.amazonaws.com'
}
FORECAST_USER_POLICY_DOCUMENT = json.dumps({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ForecastAdmin",
            "Effect": "Allow",
            "Action": [
                "forecast:*",
                "iam:ListRoles"
            ],
            "Resource": "*"
        }
    ]
})
logging.basicConfig(level=logging.INFO)


def assume_role_policy_document(forecast_service_principal):
    return json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {'Service': forecast_service_principal},
                "Action": "sts:AssumeRole"
            }
        ]
    })


def attach_forecast_policy(session, bucket_name):
    iam = session.client('iam')
    # Attach policies
    policy_name = "ForecastAccessBucket-{0}-Policy".format(bucket_name)
    policy_document = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*",
                "s3:Put*",
                "s3:DELETE*"],
            "Resource": [
                "arn:aws:s3:::" + bucket_name,
                "arn:aws:s3:::" + bucket_name + "/*"]}]})
    iam.put_role_policy(RoleName=ROLE_NAME, PolicyName=policy_name, PolicyDocument=policy_document)


# Return True if grantee already exist.
def check_kms_grantee_exist(kms, keyID, grantee):
    grant_list = kms.list_grants(KeyId=keyID)['Grants']
    for grant in grant_list:
        if grant['GranteePrincipal'] == grantee and 'Decrypt' in grant['Operations']:
            return True
    return False


def grant_decrypt(session, bucket_name, role_arn):
    # Handle encryption, only KMS is supported for now.
    s3 = session.client('s3')
    try:
        response = s3.get_bucket_encryption(Bucket=bucket_name)
        keyResponse = response['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']
        if keyResponse['SSEAlgorithm'] != 'aws:kms':
            message = "Bucket " + bucket_name + " is not encrypted with a KMS key. Please create and switch to a customer managed KMS key, and try running the script again. "
            _error(message)
        keyID = keyResponse['KMSMasterKeyID']
        kms = session.client('kms')
        keyDescription = kms.describe_key(KeyId=keyID)
        keyManager = keyDescription['KeyMetadata']['KeyManager']
        if keyManager == 'CUSTOMER':
            if check_kms_grantee_exist(kms, keyID, role_arn) is False:
                kms.create_grant(KeyId=keyID, GranteePrincipal=role_arn, Operations=['Decrypt'])
        else:
            message = "Bucket " + bucket_name + " is encrypted with AWS managed KMS key. Please create and switch to a customer managed KMS key, and try running the script again. "
            _error(message)
    except ClientError as clientError:
        if clientError.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
            logging.info("Bucket is not encrypted. Skipping KMS grants.")
        else:
            logging.error(clientError)


def get_or_create_role_arn(session, bucket_name, stage='prod'):
    role = None
    iam = session.client('iam')
    forecast_service_principal = SERVICE_PRINCIPAL_DICT[stage]
    try:
        response = iam.get_role(RoleName=ROLE_NAME)
        trust_service_dict = response["Role"]["AssumeRolePolicyDocument"]['Statement'][0]['Principal']
        if 'Service' not in trust_service_dict or trust_service_dict['Service'] != forecast_service_principal:
            logging.info("Updating service principal.")
            iam.update_assume_role_policy(RoleName=ROLE_NAME, PolicyDocument=assume_role_policy_document(forecast_service_principal))
    except NoCredentialsError as e:  # TODO see if this can be reached or remove this
        logging.error(e)
        _error('Please set up .aws locally or uncomment and fill in "aws_access_key_id" and "aws_secret_access_key".')
    except iam.exceptions.NoSuchEntityException:
        logging.info("Creating Role.")
        response = iam.create_role(RoleName=ROLE_NAME, AssumeRolePolicyDocument=assume_role_policy_document(forecast_service_principal))
        time.sleep(10)
    role = response['Role']
    role_arn = role['Arn']
    attach_forecast_policy(session, bucket_name)
    return role_arn


def validate_bucket_name(session, bucket):
    if bucket.split('/')[0] == 's3:':
        bucket = bucket.split('/')[2]
    elif bucket.split('/')[0] == 'https:':
        bucket = bucket.split('/')[3]
    s3 = session.client('s3')
    try:
        s3.head_bucket(Bucket=bucket)
    except ClientError as error:
        error_code = int(error.response['Error']['Code'])
        if error_code == 403:
            error = "Access forbidden for bucket " + bucket + "."
        elif error_code == 404:
            error = "Bucket " + bucket + " does not exist."
        _error(error)
    return bucket


def fetch_arguments():
    parser = argparse.ArgumentParser(description='Sets up the necessary permissions for Forecast.')
    parser.add_argument("bucket_name", type=str, help='S3 bucket name of format s3://<bucket_name> or <bucket_name>')
    parser.add_argument("--access_key", help="AWS Access key ID for creating the session")
    parser.add_argument("--secret_key", help="AWS Secret key for the session")
    parser.add_argument("--stage", help='Valid input: beta, gamma or prod', default='prod')

    args = parser.parse_args()

    if len([x for x in (args.access_key, args.secret_key) if x is not None]) == 1:
        parser.error('--access_key and --secret_key must be given together')
    return args.bucket_name, args.access_key, args.secret_key, args.stage


def _print_message(message, file=None):
    if message:
        if file is None:
            file = sys.stderr
        file.write(message)


def _exit(status=0, message=None):
    if message:
        _print_message(message, sys.stderr)
    sys.exit(status)


def _error(message):
    """error(message: string)
    Prints a usage message incorporating the message to stderr and
    exits.
    """
    args = {'message': message}
    _exit(2, ("Error: %(message)s\n" % args))


def get_session(access_key=None, secret_key=None):
    session = boto3.Session(
        # supply access key if needed, use an acount that has been whitelisted by Forecast
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='us-west-2'
    )
    return session


def get_user_name(iam):
    userInfo = iam.get_user()
    userName = userInfo["User"]["UserName"]
    return userName


def add_pass_role_check_policy(session, role_arn, stage='prod', userName=None):
    iam = session.client("iam")
    if userName is None:
        userName = get_user_name(iam)
    forecast_service_principal = SERVICE_PRINCIPAL_DICT[stage]
    policy_name = "PassRoleToForecastPolicy"
    policy_document = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": role_arn,
            "Condition": {
                "StringEquals": {
                    "iam:PassedToService": [
                        forecast_service_principal]}}}]})
    iam.put_user_policy(UserName=userName, PolicyName=policy_name, PolicyDocument=policy_document)
    logging.info("Attach PassRoleToForecastPolicy to User: " + userName)


def add_forecast_admin_policy(session, userName=None):
    iam = session.client("iam")
    if userName is None:
        userName = get_user_name(iam)
    policy_name = "ForecastUserPolicy"
    policy_document = FORECAST_USER_POLICY_DOCUMENT
    iam.put_user_policy(UserName=userName, PolicyName=policy_name, PolicyDocument=policy_document)
    logging.info("Attach ForecastUserPolicy to User: " + userName)


if __name__ == "__main__":
    bucket_name, access_key, secret_key, stage = fetch_arguments()
    session = get_session(access_key, secret_key)
    bucket_name = validate_bucket_name(session, bucket_name)
    role_arn = get_or_create_role_arn(session, bucket_name, stage)
    grant_decrypt(session, bucket_name, role_arn)
    add_forecast_admin_policy(session)
    add_pass_role_check_policy(session, role_arn, stage)
    logging.info("Role ARN for Forecast : %s\n" % role_arn)

# application to access AWS STS assume role
import boto3
import json
import argparse

def assume_role(role_arn):
    client = boto3.client('sts')
    response = client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='AssumeRoleSession1'
    )
    return response['Credentials']


def listS3Buckets(session):
    s3 = session.client('s3')
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(bucket['Name'])

# verify current user, session token
def verify_credentials():
    sts = boto3.client('sts')
    response = sts.get_caller_identity()
    print(json.dumps(response, indent=4, sort_keys=True, default=str))
    return sts

def changeUser(userName: str):
    home = expanduser("~")
    filename = home + AWS_CONFIG_FILE
    config = ConfigParser.RawConfigParser()
    config.read(filename)
    config.set('default', 'aws_access_key_id', userName)
    config.set('default', 'aws_secret_access_key', userName)
    with open(filename, 'w+') as configfile:
        config.write(configfile)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('target_account_id', type=str, help="Account owner of S3 bucket")
    return parser.parse_args()

'''
The current user may be an admin user linked Account A, with access key and secret access key
and temporary token to access AWS.
The target account has a role that trust the first account to do S3 full action.
'''
if __name__ == "__main__":
    args = parse_args()
    base_client=verify_credentials()
    session_role_credentials = base_client.assume_role(
        RoleArn=f"arn:aws:iam::{args.target_account_id}:role/roleForAppA",
        RoleSessionName=str("session-policy-demo"),
        DurationSeconds=900
    )
    print(session_role_credentials)
    session = boto3.session.Session(
        aws_access_key_id=session_role_credentials['Credentials']['AccessKeyId'],
        aws_secret_access_key=session_role_credentials['Credentials']['SecretAccessKey'], 
        aws_session_token=session_role_credentials['Credentials']['SessionToken']
        )
    listS3Buckets(session)
   




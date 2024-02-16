import boto3


def delete_bucket(bucket_name):
    client=boto3.client('s3')
    response = client.delete_bucket(
        Bucket=bucket_name,
    )

def delete_iam_resources(account_id,role_name,policy_name):
    iam=boto3.client('iam')
    #iam.delete_role(RoleName=role_name)
    iam.delete_policy(PolicyArn=f'arn:aws:iam::{account_id}:policy/{policy_name}')
    print("--- delete role " + role_name)
    print("--- delete policy " + policy_name)

def verify_credentials():
    sts = boto3.client('sts')
    response = sts.get_caller_identity()
    account_id = response['Account']
    user_id = response['UserId']
    return account_id, user_id


account_id, user_id = verify_credentials()
delete_iam_resources(account_id,'access-demo','app-s3-access-policy')
delete_bucket('j9r-bucket-for-app')
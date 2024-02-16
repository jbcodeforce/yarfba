import boto3,json
import logging
import argparse

DEFAULT_REGION="us-west-2"
DEFAULT_POLICY_NAME="app-s3-access-policy"

def create_S3_bucket_if_not_exists(bucket_name):
    s3 = boto3.client('s3')
    try:
        resp=s3.head_bucket(Bucket=bucket_name)
        print("--- Bucket " + bucket_name + " exists")
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print("--- Bucket " + bucket_name + " does not exist")
            print("--- Creating bucket " + bucket_name)
            resp=s3.create_bucket(Bucket=bucket_name,
                             CreateBucketConfiguration={
                                'LocationConstraint': DEFAULT_REGION,
                            },)
        else:
            raise
    return resp

def verify_credentials():
    sts = boto3.client('sts')
    response = sts.get_caller_identity()
    logging.debug(json.dumps(response, indent=4, sort_keys=True, default=str))
    account_id = response['Account']
    user_id = response['UserId']
    return account_id, user_id, sts

def create_s3_access_policy_if_not_exist(account_id:str, bucket_name: str, policy_name:str):
    if not verify_iam_policy_exists(account_id, policy_name):
        with open('bucket_policy.json', 'r') as g:
            d=json.load(g)
            policyAsString = json.dumps(d)
            policyAsString=policyAsString.replace("BUCKET_ARN", "arn:aws:s3:::"+bucket_name)
            iam = boto3.client('iam')
            resp=iam.create_policy(
                PolicyName=policy_name,
                PolicyDocument=policyAsString,
                Description='Policy to allow access to S3 bucket: ' + bucket_name
            )
            print(resp)


def verify_iam_policy_exists(account_id: str, policy_name: str):
    try:
        iam = boto3.client('iam')
        iam.get_policy(PolicyArn=f"arn:aws:iam::{account_id}:policy/{policy_name}")
        print("--- Policy " + policy_name + " exists")
        return True
    except iam.exceptions.NoSuchEntityException:
        print("--- Policy " + policy_name + " does not exist")
        return False

def create_role_for_app_if_not_exist(account_id: str,role_name: str,partner_account_id):
    iam = boto3.client('iam')
    try:
        iam.get_role(RoleName=role_name)
        print("--- role " + role_name + " exists")
    except iam.exceptions.NoSuchEntityException:
        print("--- creating role " + role_name)
        create_role(iam,role_name,partner_account_id)

def create_role(iam,role_name,partner_account_id):
    with open("trust_relation.json",'r') as f:
        d=json.load(f)
        policyAsString = json.dumps(d)
        policyAsString=policyAsString.replace("<partner_account>",partner_account_id)
        print(policyAsString)
        resp=iam.create_role(RoleName=role_name,
                             AssumeRolePolicyDocument=policyAsString,
                             Description='A role for app in Account A to assume',)
        print(resp)
        

def attach_s3_access_policy_to_role(account_id: str, role_name: str, policy_name: str):
    iam=boto3.client('iam')
    try:
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=f"arn:aws:iam::{account_id}:policy/{policy_name}")
        print("--- Policy " + policy_name + " attached to role " + role_name)
    except iam.exceptions.NoSuchEntityException:
        print("--- Policy " + policy_name + " already attached")
       

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('bucket_name', type=str, default="j9r-bucket-for-app")
    parser.add_argument('target_account_id', type=str)
    return parser.parse_args()


'''
Be connected on Account B with Admin user
Input arguments:
    - bucket_name: name of the bucket to be created the bucket_name
    - target_account_id: the account id of the account A
'''
if __name__ == '__main__':
    args = parse_args()
    print("Be connected on Account B with Admin user")
    account_id, user_id, sts=verify_credentials()
    print(f"User {user_id} from Account ID: {account_id} will create s3 bucket, new role and policy")
    resp=create_S3_bucket_if_not_exists(args.bucket_name)
    create_s3_access_policy_if_not_exist(account_id,args.bucket_name,DEFAULT_POLICY_NAME)
    create_role_for_app_if_not_exist(account_id, "roleForAppA",args.target_account_id)
    attach_s3_access_policy_to_role(account_id, "roleForAppA", DEFAULT_POLICY_NAME)







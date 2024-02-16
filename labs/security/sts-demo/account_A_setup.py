import boto3, json, argparse


def create_role(role_name,account_id):
    iam=boto3.client("iam")
    try:
        iam.get_role(RoleName=role_name)
        print("--- role " + role_name + " exists")
    except iam.exceptions.NoSuchEntityException:
        print("--- create role " + role_name)
        with open("A_trust_relation.json",'r') as f:
            d=json.load(f)
            policyAsString = json.dumps(d)
            policyAsString=policyAsString.replace("<account_id>",account_id)       
            resp=iam.create_role(RoleName=role_name,
                                AssumeRolePolicyDocument=policyAsString,
                                Description='A role for app in Account A to assume',)
            print(resp)

def verify_credentials():
    sts = boto3.client('sts')
    response = sts.get_caller_identity()
    account_id = response['Account']
    user_id = response['UserId']
    return account_id, user_id


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('app_role_name', type=str,  default="appRole")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print("Be connected on Account A with Admin user")
    account_id, user_id=verify_credentials()
    create_role(args.app_role_name, account_id)
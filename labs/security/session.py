import boto3

from os.path import expanduser
import ConfigParser

print ('\n\n--------------------------HOW TO--------------------------------------')
print ('sts:assumerole* allows a user or system to inject a policy to further restrict the user\'s permission during that session. To demonstrate this the script will prompt you for the following: \n\n')
print('Base Profile \t\t This is the profile that will be used to assume the role that the session policy will be applied on. This role / user need the sts:assume permission on the session role.')
print('Session Profile \t The script will store the new session in your AWS credentials file under this name.')
print('AWS Region \t\t Will add the region to the credentials file.')
print('Role to assume \t\t This is the role that the base role will assume and apply the session policy to. This demo works best on a administrative type role.')
print('Session Policy Arn \t The policy that will be overlayed on the session. This will default to the AWS managed policy for S3 read access. Note this policy needs to be in the same account as the role that will be assumed.')
print ('----------------------------------------------------------------------\n\n')

AWS_CONFIG_FILE = '/.aws/credentials'

AWS_CLI_BASE_PROFILE = raw_input('Base Profile [default]:') or 'default'
SESSION_PROFILE_NAME = raw_input('Store Session\'d Profile As [session_test]:') or 'session_test'
REGION = raw_input('AWS Region [eu-west-1]:') or 'us-west-2'

ROLE_TO_ASSUME_WITH_SESSION = raw_input('Role ARN To Assume:')
SESSION_POLICY_ARN = raw_input('Session Policy Arn [arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess]:') or 'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'

print ('\n\n--------------------------CONFIG--------------------------------------')
print('Base Profile \t\t {0}'.format(AWS_CLI_BASE_PROFILE))
print('Session Profile \t {0}'.format(SESSION_PROFILE_NAME))
print('AWS Region \t\t {0}'.format(REGION))
print('Role to assume \t\t {0}'.format(ROLE_TO_ASSUME_WITH_SESSION))
print('Session Policy Arn \t {0}'.format(SESSION_POLICY_ARN))
print ('----------------------------------------------------------------------\n\n')

base_profile_cli_creds = boto3.session.Session(profile_name=AWS_CLI_BASE_PROFILE, region_name=REGION)
base_client = base_profile_cli_creds.client('sts')

session_role_credentials = base_client.assume_role(
    RoleArn=ROLE_TO_ASSUME_WITH_SESSION,
    RoleSessionName=str("session-policy-demo"),
    PolicyArns = [{
        'arn': SESSION_POLICY_ARN
    }],
    DurationSeconds=900
    )

session_credentials = session_role_credentials['Credentials']

# Write the new token to AWS credentials file
home = expanduser("~")
filename = home + AWS_CONFIG_FILE

config = ConfigParser.RawConfigParser()
config.read(filename)

if not config.has_section(SESSION_PROFILE_NAME):
    config.add_section(SESSION_PROFILE_NAME)

config.set(SESSION_PROFILE_NAME, 'output', 'json')
config.set(SESSION_PROFILE_NAME, 'region', REGION)
config.set(SESSION_PROFILE_NAME, 'aws_access_key_id', session_credentials['AccessKeyId'])
config.set(SESSION_PROFILE_NAME, 'aws_secret_access_key', session_credentials['SecretAccessKey'])
config.set(SESSION_PROFILE_NAME, 'aws_session_token', session_credentials['SessionToken'])

with open(filename, 'w+') as configfile:
    config.write(configfile)

print ('\n\n---------------------------RESULT-------------------------------------')
print ('Your new access key pair has been stored in the AWS configuration file {0} under the {1} profile.'.format(filename, SESSION_PROFILE_NAME))
print ('Note that it will expire at {0}.'.format(session_credentials['Expiration']))
print ('After this time, you may safely rerun this script to refresh your access key pair.')
print ('To use this credential, call the AWS CLI with the --profile option (e.g. aws --profile {0} ec2 describe-instances).'.format(SESSION_PROFILE_NAME))
print ('----------------------------------------------------------------------\n\n')

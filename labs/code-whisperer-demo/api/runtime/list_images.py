import boto3,os

TABLE_NAME = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # scan dynamodb for all items    
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    return response['Items']
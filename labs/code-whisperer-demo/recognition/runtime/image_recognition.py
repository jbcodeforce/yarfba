import boto3
import uuid

def handler(event, context):
    # 1. Read message from SQS
    message = receive_message_from_sqs('test-queue')
    
    # 2. use Amazon recognition to recognize the image
    labels = detect_labels(message[0].body['bucket'], message[0].body['key'])  
    # 3. persist in dynamoDB
    persist_items_to_dynamo(uuid.uuid4(), labels)
    # 4. send message to SNS
    send_message_to_sns(labels,'test-topic')
    # 5. delete message from SQS
    delete_message_from_sqs('test-queue','receipt_handle')
    


    return { 'statusCode': 200, 'body': 'Success'}

# define a function to receive message from sqs
def receive_message_from_sqs(sqs_queue_name):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='test-queue')
    message = queue.receive_messages(
        MessageAttributeNames=['All'],
        MaxNumberOfMessages=1
    )
    return message

# save items to dynamoDB
def persist_items_to_dynamo(image_id,labels):
    item = {
        'image_id': image_id,
        'labels': labels
    }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('test-table')
    table.put_item(Item= item)
    return True
    

# detect labels in an image
# return a list of labels
def detect_labels(bucket, key):
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        },
        MaxLabels=10,
        MinConfidence=75
    )
    return response['Labels']

# define a send message to sns function
def send_message_to_sns(message, topic_arn):
    sns = boto3.client('sns')
    sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='Image Recognition')

# delete message from sqs
def delete_message_from_sqs(queue_url,receipt_handle):
    sqs = boto3.resource('sqs')
    queue = sqs.Queue(queue_url)
    resp = queue.delete_messages(
        Entries=[
            {
                'Id': receipt_handle,
                'ReceiptHandle': receipt_handle
            }
        ]
    )
    return resp

    
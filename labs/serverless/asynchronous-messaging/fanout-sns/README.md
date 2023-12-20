# Fan out pattern

![](https://static.us-east-1.prod.workshops.aws/public/55bcfbea-5e82-4f49-be25-22c3a9740719/static/fan-out-and-message-filtering/bootstrap-initial-state/step-1.png)

It deployes: Unicorn Management service (leveraging Amazon API Gateway  and AWS Lambda ), the Rides Store (leveraging Amazon DynamoDB ) and three Serverless backend services - Customer notification, Customer accounting, and the Extraordinary rides service.
The Main management service, called from the API Gateway, uses two policies: to CRUD on Dynamodb table and publish to SNS topic.

The Lambda publishes to SNS using boto3

```python
response = sns.publish(
    TopicArn=TOPIC_ARN,
    Message=json.dumps(request),
    MessageAttributes = {
        'fare': {
            'DataType': 'Number',
            'StringValue': str(request['fare'])
        },
        'distance': {
            'DataType': 'Number',
            'StringValue': str(request['distance'])
        }
    }
)
```

Each service subscribes to the SNS topic

```yaml
  CustomerNotificationFunction:
    Type: AWS::Serverless::Function 
    Properties:
      CodeUri: customer_notification_service/
      Handler: app.lambda_handler
      Events:
       SNSEvent:
         Type: SNS
         Properties:
           Topic: !Ref RideCompletionTopic 
```

* Final SAM template is in [labs/serverless/asynchronous-messaging/fanout-sns](https://github.com/jbcodeforce/aws-studies/tree/main/labs/serverless/asynchronous-messaging/fanout-sns) with readme to demonstrate quickly the deployment.


## Deploy

```sh
sam build
export AWS_REGION=$(aws --profile default configure get region)
sam deploy \
    --stack-name wild-rydes-async-msg-1 \
    --capabilities CAPABILITY_IAM \
    --region $AWS_REGION \
    --guided 
```

Confirm the first 5 proposed arguments by hitting ENTER. When you get asked SubmitRideCompletionFunction may not have authorization defined, Is this okay? [y/N]:, enter y and hit ENTER for remaining options.

## Test

```sh
export ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name wild-rydes-async-msg-1 \
    --query 'Stacks[].Outputs[?OutputKey==`UnicornManagementServiceApiSubmitRideCompletionEndpoint`].OutputValue' \
    --output text)

curl -XPOST -i -H "Content-Type\:application/json" -d '{ "from": "Berlin", "to": "Frankfurt", "duration": 420, "distance": 600, "customer": "cmr", "fare": 256.50 }' $ENDPOINT

```

## Explanations

### Security

The stack is creating the security roles which use LambdaBasicExecution policies so each lambda function is able to write to CloudWatch log group.

## Clean up

* Delete the stack

```sh
aws cloudformation delete-stack \
    --stack-name wild-rydes-async-msg-1
```

* Delete the logs

```sh
aws logs describe-log-groups --query 'logGroups[*].logGroupName' --output table | awk '{print $2}' | \
    grep ^/aws/lambda/wild-rydes-async-msg-1 | while read x; \
    do  echo "deleting $x" ; aws logs delete-log-group --log-group-name $x; \
done
```
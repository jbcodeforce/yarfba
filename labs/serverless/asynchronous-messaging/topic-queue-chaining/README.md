## Topic queue chaining

The goal is to avoid subscriber missing message from te SNS topic, so the approach is to add queue between the SNS topic and the subscriber. 

![](https://static.us-east-1.prod.workshops.aws/public/55bcfbea-5e82-4f49-be25-22c3a9740719/static/topic-queue-chaining-and-load-balancer/module-2.png)

As messages are buffered in a persistent manner in an SQS queue, no message will get lost should a subscriber process run into problems for many hours or days, or has exceptions or crashes.

Also queue can act as a buffering load-balancer.


And the main service configuration in CloudFormation:

```yaml
  SubmitRideCompletionFunction:
    Type: AWS::Serverless::Function 
    Properties:
      CodeUri: unicorn-management-service/
      Handler: app.lambda_handler
      Environment:
        Variables:
          TABLE_NAME: !Ref RidesTable
          TOPIC_ARN: !Ref RideCompletionTopic
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref RidesTable
        - SNSPublishMessagePolicy: 
           TopicName: !GetAtt RideCompletionTopic.TopicName
      Events:
        WildRydes:
          Type: Api 
          Properties:
            Path: /submit-ride-completion
            Method: post
```

Queue can subscribe to SNS from the Console or via CF template

```yaml
RideCompletionTopic:
   Type: AWS::SNS::Topic
   Properties:
     TopicName: RideCompletionTopic
CustomerAccountingServiceQueue:
   Type: AWS::SQS::Queue
CustomerAccountingServiceQueueToRidesTopicSubscription:
   Type: AWS::SNS::Subscription
   Properties:
      Endpoint: !GetAtt CustomerAccountingServiceQueue.Arn
      Protocol: sqs
      RawMessageDelivery: true
      TopicArn: !Ref RideCompletionTopic

```

And each consumer service subscribes to the SQS queue

```yaml
  CustomerAccountingService:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: generic-backend-microservice/
      Handler: app.lambda_handler
      ReservedConcurrentExecutions: 5
      Environment:
        Variables:
          SERVICE_NAME: CustomerAccountingService
      Policies:
       - SQSPollerPolicy:
           QueueName: !Ref CustomerAccountingServiceQueue
      Events:
       CustomerAccountingServiceJobQueue:
         Type: SQS
         Properties:
            Queue: !GetAtt CustomerAccountingServiceQueue.Arn
            BatchSize: 1
```

## Deploy

```sh
sam build
export AWS_REGION=$(aws --profile default configure get region)
sam deploy \
    --stack-name wild-rydes-async-msg-2 \
    --capabilities CAPABILITY_IAM \
    --region $AWS_REGION \
    --guided 
```

Confirm the first 5 proposed arguments by hitting ENTER. When you get asked SubmitRideCompletionFunction may not have authorization defined, Is this okay? [y/N]:, enter y and hit ENTER for remaining options.

## Test

```sh
export ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name wild-rydes-async-msg-2 \
    --query 'Stacks[].Outputs[?OutputKey==`UnicornManagementServiceApiSubmitRideCompletionEndpoint`].OutputValue' \
    --output text)

curl -XPOST -i -H "Content-Type\:application/json" -d '{ "from": "Berlin", "to": "Frankfurt", "duration": 420, "distance": 600, "customer": "cmr", "fare": 256.50 }' $ENDPOINT

```

## Understanding the log

Looking at a consumer service, some of those service will create an exception so the response /acknowledge is not sent back to the queue, and the message is not removed from the queue, therefore the SQS service push it later using retries.

## Clean up

* Delete the stack

```sh
aws cloudformation delete-stack \
    --stack-name wild-rydes-async-msg-2
```

* Delete the logs

```sh
aws logs describe-log-groups --query 'logGroups[*].logGroupName' --output table | awk '{print $2}' | \
    grep ^/aws/lambda/wild-rydes-async-msg-2 | while read x; \
    do  echo "deleting $x" ; aws logs delete-log-group --log-group-name $x; \
done
```
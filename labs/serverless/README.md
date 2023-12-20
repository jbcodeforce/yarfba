# Serverless Worshops

This folder includes the code to  quickly demonstrating the  different serverless workshops.

## Serverless patterns

Folder: [labs/serverless/ws-serverless-patterns](https://github.com/jbcodeforce/aws-studies/tree/main/labs/serverless/ws-serverless-patterns)

Once the sam deploy is done (`sam build && sam deploy --guided --stack-name ws-serverless-patterns`), things to demonstrate:

* See the DynamoDB `ws-serverless-patterns-Users` table created with users in it. Use AWS console to go to the DynamoDB page - or following CLI 

    ```sh
    aws dynamodb scan --table-name ws-serverless-patterns-Users
    ```

* Can test the lambda function locally: `sam local invoke -e events/event-put-user.json -n env.json`. Verify the created user

    ```sh
    aws dynamodb get-item --table-name ws-serverless-patterns-Users --key '{"userid": {"S": "<userid-from-response>"}}' 
    ```
* Use Cognito login URL to register a user.    
* Demonstrate users in Cognito using AWS Console or do the following

    ```sh
    aws cognito-idp list-user-pools --max-results 2
    aws cognito-idp list-groups --user-pool-id us-west-2_h....
    aws cognito-idp list-users --user-pool-id us-west-2_h....
    ```

* Validate the API Gateway of the user resource could not be accessed via: `curl https://6......e.execute-api.us-west-2.amazonaws.com/Prod/users`. Need to get a JWT `token` and user `sub` information then add it to the url:

    ```sh
    # 1- get the client id for Cognito-idp from the cloud formation outputs
    # 2- Get the token
    aws cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH --client-id 4.....n  --auth-parameters USERNAME=<email address of one of cognito user>,PASSWORD=<user-password>
    # 3- Copy the IdToken field to environment variable
    export ID_TOKEN=
    # 4- test with authorization - 
    curl <API_Endpoint>/users -H "Authorization:$ID_TOKEN"
    # 5- Use jwt.io web site to get the principalId information from the token and field cognito:username 
    https://jwt.io
    #6- try with the principal
    curl https://<API_Endpoint>/users/f8.....6b  -H "Authorization:$ID_TOKEN"
    # You should not receive authentication or authorization errors, just an empty response: {} because there is not records in DynamoDB users tables with the principal ID. 
    ```

* Verify with Unit testing: 

    ```sh
    source .venv/bin/activate
    pip install -r requirements.txt
    pip install -r ./tests/requirements.txt
    python -m pytest tests/unit -v`
    ```

* Verify with integration tests to the development environment cloud:

    ```sh
    export ENV_STACK_NAME=ws-serverless-patterns
    python -m pytest tests/integration -v
    ```

* Observe the application, going to the X-Ray console to see the end to end tracing.
* Verify the alarms set and that use SNS to send message. Send a message every time any error is logged on the API Gateway in the past minute. Same for Lambda authorizer and users lambdas. Or when one of the lambda is throttled. Be sure to have created a subscription to the SNS topic.

    ```sh
    aws lambda put-function-concurrency     --function-name   ws-serverless-patterns-UsersFunction-11....   --reserved-concurrent-executions 40
    python -m pytest tests/integration -v
    ```

* Display CloudWatch dashboard:  The dashboard will include widgets for API Gateway and Lambda metrics. 

For the CI/CD change the account_ID in the `codepipeline.yaml` and default parameters to reflect new resources.

## Decoupled Microservices

[Git repo for code source.](https://github.com/aws-samples/asynchronous-messaging-workshop/tree/master/code/lab-1), completed work is under [labs/serverless/asynchronous-messaging](ttps://github.com/jbcodeforce/aws-studies/tree/main/labs/serverless/asynchronous-messaging)

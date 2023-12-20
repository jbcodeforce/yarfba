# A simple solution

The solution looks like in the folliwing diagrams

We can use two ways to test the solution locally. To develop the function use the `aws-strfunctions-local` docker image

## With Step Function Local

* Start the step function executor

```sh
docker run -d -p 8083:8083 amazon/aws-stepfunctions-local
```

* Create the function, with a dummy role. If the flow does not include call to Lambda.

```sh
aws stepfunctions --endpoint-url http://localhost:8083 create-state-machine --definition "$(jq -Rs '.' ./statemachine/credit_approval.asl.json) --name "HelloWorld" --role-arn "arn:aws:iam::00000000:role/DummyRole"" 
```

* When we need to interact with Lambda, use sam local to start the lambdas. see https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local-lambda.html.

```sh
sam local start-api
```

## With SAM

* Created via SAM: `sam init`

It includes the following files and folders:

- functions - Code for the application's Lambda functions to check the value of, buy, or sell shares of a stock.
- statemachines - Definition for the state machine that orchestrates the stock trading workflow.
- tests - Unit tests for the Lambda functions' application code.
- template.yaml - A template that defines the application's AWS resources.

* Use AWS Toolkit for VS Code for state machine visualization
* Start LocalStack with `docker compose up -d`
* Install pre-requisites library as:

```sh
pip install awscli
pip install awscli-local
pip install aws-sam-cli-local
```

* To build and deploy the application for the first time, run the following in a shell:

```bash
samlocal build 
samlocal deploy 
```

* Verify the resources created:

```sh
awslocal cloudformation list-stacks
# IAM roles
awslocal iam list-roles
# Lambda functions
awslocal lambda list-functions
#
awslocal stepfunctions list-state-machines
```

* Invoke one of the lambda function defined, we should get an integer between 1 and 10,000.

```sh
samlocal local invoke 
```

* In case something goes wrong

```sh
docker compose down
rm -r volumes
rm -r .aws_sam
```

* Assess the step function created:

```sh
awslocal stepfunctions describe-state-machine --state-machine-arn "arn:aws:states:us-west-2:000000000000:stateMachine:CreditApprovalProcessFlow"
```

* Execute it

```sh
awslocal stepfunctions start-execution --name test --state-machine-arn "arn:aws:states:us-west-2:000000000000:stateMachine:CreditApprovalProcessFlow"
```

we should get the execution arn

```json
{
    "executionArn": "arn:aws:states:us-west-2:000000000000:execution:CreditApprovalProcessFlow:test",
    "startDate": 1695165250.151
}
```

* Check the result:

```sh
awslocal stepfunctions describe-execution --execution-arn arn:aws:states:us-west-2:000000000000:execution:CreditApprovalProcessFlow:....
```

* To update a state machine definition. As the definition needs to be single json string, we need to transform the file using `jq`. The updateFlow.sh is doing the update.



## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
step-sol-1$ pip install -r tests/requirements.txt --user
# unit test
step-sol-1$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
step-sol-1$ AWS_SAM_STACK_NAME="step-sol-1" python -m pytest tests/integration -v
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
sam delete --stack-name "step-sol-1"
```
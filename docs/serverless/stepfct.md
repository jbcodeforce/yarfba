# [AWS Step Function](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)

AWS Step Functions is a fully managed service that we can use to coordinate the components of distributed applications and microservices using visual workflows. 

## Value propositions

* Resilient workflow automation
* Built-in error handling
* AWS service integration
* Auditable execution history and visual monitoring
* Serverless, can scale by itself
* Support short execution flow, or long lived transactions.
* Standard Workflows follow an **exactly-once** model, while Express Workflows employ an **at-least-once** model when called asynchronously, and **at-most-once** with synchronous call (message may be lost). [Important differentiations.](https://docs.aws.amazon.com/step-functions/latest/dg/express-at-least-once-execution.html)
* Reuse business logic in different flows
* Standard is billed by the # of state transitions while express by the number of executions, the duration of execution, and the memory consumed.
* Support a Map operation/state to run a set of workflow steps for each item in a dataset, in parallel. With **inline** mode maps runs in the context of the workflow. With **distributed** each map state runs in a child workflow execution, in parallel (scale to more than 40 parallel iterations).

## Concepts

The workflow is defined using the [State Language Notation](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html). 

* All work in Step Functions is done by **tasks**. 
* A task performs work by using an activity or an AWS Lambda function, or by passing parameters to the API actions of other services. 
* An **activity** is an application that we write and host on AWS, on premises or on mobile devices. 
* Activity **workers** execute the application code and report success or failure.
* The patterns supported are sequential sequencing of tasks, conditional branching, looping task, try-catch-finally for error and compensation, parallel execution.
* A `Task` state ("Type": "Task") represents a single unit of work performed by a state machine.
* Can integrate Human task. 
* They are long running flow. But there is also the **Express Workflow** that is a short duration execution to support 100k state transitions per sec. ( Duration has to be less than 5 mins). It saves states in memory.
* When calling external service, one of the parameter is the `TaskToken` to send back to the Step service so the corresponding task can get the asynch response.
* For Standard workflow the max duration is 365 days.
* Input data can be pass in StartExecution call. 
* For Standard Workflows, you can retrieve execution results from the execution history using external callers, such as the `DescribeExecution` action (`awslocal stepfunctions describe-execution --execution-arn ...` ).
* A `path` is a string beginning with `$` that you can use to identify components within JSON text.
* `InputPath` can limit the input that is passed by filtering the JSON notation by using a path
* `OutputPath` enables you to select a portion of the state output to pass to the next state. 

## Integration

* Step can be started from HTTP requests from APIGTW, IoT Rules, EventBridge, Lambda...
* For asynchronous express workflows (SDK StartExecution), to get the results we must poll cloudwatch logs.
* Step function uses a context object to keep, in JSON, the state of the state machine execution. 

???- info "Call Lambda"
    Need a reference to the function ARN, and then stipulates the input, output parameters and retries logic. The Parameter for "Payload.$": "$" takes the input and send that to the lambda.
    ```json
    "Get credit limit": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "Payload.$": "$",
        "FunctionName": "arn:aws:lambda:us-west-2:000000000000:function:GetCreditLimit"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 2,
          "MaxAttempts": 6,
          "BackoffRate": 2
        }
      ],
      "Next": "Credit applied >= 5000?"
    },
    ```

## Error Handling

Step Functions supports errors and retries via a looping pattern and provides try/catch/finally logic for known or unknown errors.

At a high level, task and parallel states can use fields named **Retry and Catch** for error handling. When a state reports an error and there is no Retry or the retries don’t resolve the problem, Step Functions looks through the catchers for a matching error and transitions to the state named in the next field. 

Each catcher can specify multiple errors to handle. The reserved name `States.ALL` is a wildcard that matches any error name.

## Hands-on demo

We can use [LocalStack](https://docs.localstack.cloud/user-guide/aws/stepfunctions/) to start developing Step function in vscode and run locally. See the [labs/step/first-solution](https://github.com/jbcodeforce/aws-studies/tree/main/labs/step/first-solution)

### Basic Step flow to Lambda call

See the Lab in [labs/step/step2lambda folder](https://github.com/jbcodeforce/aws-studies/tree/main/labs/step/step2lambda).

### Simple solution

This demo includes all the basic control flow constructs for a worflow: call lambda, read from DynamodDB, and perform Map computation. See the [labs/step/first-solution](https://github.com/jbcodeforce/aws-studies/tree/main/labs/step/first-solution).


### Image processing from S3

Image processing for Autonomous car: upload traveller's shelfie photos, to build a collection against it a camera can send a new image to recognize the traveller's face so he/she can enter in the car. This example is based on the [image processing with step function workshop](https://www.image-processing.serverlessworkshops.io/). See [this repo](https://github.com/jbcodeforce/traveller-recognition.git) for SAM / CloudFormation templates and function code.

## [Step Function FAQs](https://aws.amazon.com/step-functions/faqs/)

* Where process instance information is persisted for the running workflows?
* How to support re-entrance?
* How to support DR

## Expected Skill Set

???- question "What are the different state types?"
    Pass, Task, Choice, Wait, Succeed, Fail, Parallel, Map.


## Deeper dive

* [Main product marketing page](https://aws.amazon.com/step-functions)
* [10 mns getting started](https://aws.amazon.com/step-functions/getting-started/#Tutorials)
* [Information resources like reference architecture](https://aws.amazon.com/step-functions/resources)
* [How step functions work.](https://explore.skillbuilder.aws/learn/course/internal/view/elearning/9241/how-aws-step-functions-work)
* [Design pattern for step functions.](https://explore.skillbuilder.aws/learn/course/internal/view/elearning/10471/design-patterns-for-aws-step-functions)
* [Git repo with Step Function examples defined as CloudFormation templates.](https://github.com/aws-samples/aws-stepfunctions-examples)
* [Developer guide.](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
* [VScode extension with visualization](https://aws.amazon.com/blogs/compute/aws-step-functions-support-in-visual-studio-code/)
* [Step function workshop](https://catalog.workshops.aws/stepfunctions/en-US).
* [Saga with State machine](https://github.com/aws-samples/aws-step-functions-long-lived-transactions).
* [Create serverless workflow with Step - hands-on tutorial 10 minutes](https://aws.amazon.com/getting-started/hands-on/create-a-serverless-workflow-step-functions-lambda/)
# A set of personal labs to go deeper on some AWS services


## AWS Cloud9

Try to use AWS Cloud9 to do most of the labs, as it avoids creating internet endpoints. Some helpful tricks:

* Verify the environment with `aws  sts get-caller-identity`
* Get access to a web app

## IAM - Organization - Security

* [User assuming a new role](./security/index.md) demonstration to access EC2 using trusted relationship, and IAM policies.
* [IAM and AWS Organization for cross account access](https://github.com/jbcodeforce/aws-organization-play) in separate git repository.
* An Attribute based access control tutorial, in [labs/security/iam/abac folder](https://github.com/jbcodeforce/aws-studies/tree/main/labs/security/iam/abqc) with cdk to do the tutorial.

## CloudFormation

* A Redis Server in a VPC, public subnet. See [labs/networking](https://github.com/jbcodeforce/aws-studies/tree/main/labs/networking).

## CDK play

* A complete app with Lambdas, API Gateway, DynamoDB table demonstrating how to chain lambda functions. It is part of a [AWS cdk workshop](https://github.com/jbcodeforce/aws-studies/tree/main/labs/cdk/cdk_workshop). One Lambda is a basic hello world and the second one is counting each request to hello and increase a counter in DynamoDB. The hit count function is exposed as part of API Gateway `/` path. Once receive the event, it delegates to hello function to get the response, but update the dynamodb table before that. It also uses cdk-dynamo-table-view to view the content of a table. There are also access control to authorize the hello lambda to call the 
*  The [ec2-vpc](https://github.com/jbcodeforce/aws-studies/tree/main/labs/cdk/ec2-vpc) folder supports the following definitions:

    ![](./diagrams/hands-on-vpc.drawio.svg)

* [ec2-basic](https://github.com/jbcodeforce/aws-studies/tree/main/labs/cdk/ec2-basic): use API to get reference to the default VPC then create `t2.micro` EC2 instance to host Apache httpd as defined in a user_data script.

* [cdk/kinesis](https://github.com/jbcodeforce/big-data-tenant-analytics/tree/main/cdk/kinesis)
* [cdk for a python app on EC2 using user-data to start it](https://github.com/jbcodeforce/aws-cdk-project-templates/tree/main/EC2pythonAppStack)
* [Prompt-engineering in llm-ref-arch-demo repo:](https://github.com/jbcodeforce/llm-ref-arch-demo/tree/main/prompt-engineering) A CDK with an ALB to ECS Fargate service and task running a Streamlit app


## Analytics

* EMR serverless demo to do product recommendations [emr-serverless-demo](https://github.com/jbcodeforce/aws-studies/tree/main/labs/analytics/emr-serverless-demo) and then with EMR cluster and EMR Studio/ Notebook. [emr-ec2-demo](https://github.com/jbcodeforce/aws-studies/tree/main/labs/analytics/emr-ec2-demo)

* EMR getting started in [labs/analytics/emr-starting](https://github.com/jbcodeforce/aws-studies/tree/main/labs/analytics/emr-starting). The goal is to process food establishment inspection data.
* In [emr-cdk-analytics](https://github.com/jbcodeforce/aws-studies/tree/main/labs/analytics/emr-cdk-analysis) EMR cluster in a dedicated VPC, with S3 bucket to get scripts from it. IAM role on emr principal with a custom policy to read from the s3 bucket, so our EMR can access S3. Then a IAM role for the emr job, as ec2 principal. An instance profile is also used in the EMR cluster definition. The cluster includes Core node on EC2 reserved instance and spots for master node. It includes the script to be executed in a job.
* [Analytics/emr-serverless](https://github.com/jbcodeforce/aws-studies/tree/main/labs/analytics/emr-serverless) includes aws cli scripts to define emr cluster, and submit job using python script to count word in a text, uploaded to a s3 bucket. It also include a cloud formation for a cloud watch dashboard. 

* [Analytics/kinesis-getting-started](https://github.com/jbcodeforce/aws-studies/tree/main/labs/analytics/kinesis-getting-started): Writing to an Amazon S3 Bucket from Kinesis data analytics using AWS CLI.

## Athena

## Lambda

* [S3 file processing with a Lambda.](https://github.com/jbcodeforce/aws-studies/tree/main/labs/lambdas/s3-lambda) 
* [A java lambda with CDK deployment](https://github.com/jbcodeforce/aws-studies/tree/main/labs/lambdas/java-sample) to process weather record.
* [Car rides generator with python Lambda](https://github.com/jbcodeforce/CarRideGenerator)
* [Repo to illustrate Getting GitHub events to API gtw, Lambda and Slack in Python](https://github.com/jbcodeforce/from-git-to-slack-serverless)

## Active MQ and messagings

* [Repo aws-messageing-study](https://github.com/jbcodeforce/aws-messaging-study)
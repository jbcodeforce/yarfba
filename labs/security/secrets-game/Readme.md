# AWS Secrets manager play with quarkus app

The goal is to create secrets using Cloud Formation, then to use a python app to load the secret content.

This is based on [Serverland Secrets Manager with Fargate](https://serverlessland.com/patterns/cdk-fargate-secrets-manager?ref=search)

The app folder includes a simple Python app to be packaged as container for deployment to ECR.
 
The CDK code, in `infrastructure` folder creates Amazon ECS Cluster, ECS Task Definition for the python App, AWS Fargate Container, and AWS Secrets Manager instance, along with associated roles.

## Run locally using LocalStack

Quarkus Amazon Services automatically starts a LocalStack container in dev mode and when running test. Dev Services for Amazon Services is automatically enabled for each extensions added to pom.xml.

* Create an aws profile call `localstack` with `aws configure`. The region needs to match the value in the application.properties of the quarkus app, if not the localstack will create two secrets manager and it will be confusing.

```sh
aws configure
[localstack]
aws_access_key_id = test-key
aws_secret_access_key = test-secret
region=us-east-1
```

* Start docker compose with a localstack with port 4566

```sh
# under app
docker compose up
```

* Start the Quarkus app

```sh
quarkus dev
```

* Get the end point for the started container (docker ps), then try to use a command like the following by specifying the end point:

```sh
awslocal secretsmanager list-secrets --endpoint-url http://localhost:4566 --profile localstack
```

* Create a secret:

```sh
awslocal secretsmanager create-secret --name test-secret --description "quarkus app Secret" --secret-string file://$(pwd)/secret.json  --endpoint-url http://localhost:4566 --profile localstack
```

* Validate it

```sh
awslocal secretsmanager describe-secret --secret-id test-secret --endpoint-url http://localhost:4566 --profile localstack
```

* List all secrets

```sh
awslocal secretsmanager list-secrets --endpoint-url http://localhost:4566 --profile localstack
```

* Accessing the secret via the quarkus app to get the same results

```
curl -X GET http://localhost:8080/secrets/list
```

* Use the Post on the secrets resource:

```sh
./e2e/portAsecret.sh
```

* Verify the new added with `curl -X GET http://localhost:8080/secrets/AppDemo`

* Stop

```sh
docker compose down
```

## Package and push to docker hub

Under app folder:

```sh
./buildAll.sh
```

## Deploy the cdk stack to AWS

* Under infrastructure folder:

```sh
cdk deploy
```


* Undeploy

```sh
cdk destroy
```

## Source of info:

* [Tutorial: Specifying Sensitive Data Using Secrets Manager Secrets](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data-tutorial.html)
* [Quarkus AWS](https://docs.quarkiverse.io/quarkus-amazon-services/dev/amazon-secretsmanager.html)
* [AWS LocalStack](https://docs.localstack.cloud/overview/)
* [LocalStack secrets manager doc.](https://docs.localstack.cloud/user-guide/aws/secretsmanager/)
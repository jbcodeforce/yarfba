# A code template for Java Lambda packaged as docker image

The code is based on a WeatherData bean, the lambda changes the status of the data and logs it.

## Build

* Create ECR repository

```sh
./scripts/createECRrepository.sh
```
* Be sure to be logged in the ECR service:

```sh
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <ecr-endpoint>.amazonaws.com
```

* Build with the command

```sh
./scripts/buildAll.sh ......dkr.ecr.us-west-2.amazonaws.com
```

* Test it locally

```sh
docker run -p 9000:8080 jbcodeforce/java-lambda 
```

Then a curl to the endpoint: `2015-03-31/functions/function/invocations`

```sh
curl -XPORT http://localhost:9000/2015-03-31/functions/function/invocations  -d "{'temperatureK': 123, 'windKmh': 30, 'humidityPct': 0.6, 'pressureHPa': 1024}" 
```

## Deploy the function using CDK

* Start python with cdk docker image

```sh
../../startPythonDocker.sh

```

* In the bash within the container:

```sh
cdk deploy
```

* Once deployed, in the Lambda console, define an event in the format of the WeatherData and test the function locally. The status should be changed to `Processed`.
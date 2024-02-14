# Example of EventBridge to different targets

This is an example based on the EDA Workshop but re-factorized to put the elements at the good place, applying clear separation of concerns, and integrating the manual steps of the lab as cloud formation resources.

The solution looks like:

## Create the full solution stack

```sh
aws cloudformation create-stack --stack-name aws-event-driven-architectures-workshop --template-body file://master-v2.yaml --parameters ParameterKey=KeyPairName,ParameterValue=TestKey
```

TO DO

* integrate event bridge event bus definition with the 3 rules
* build a simple master without event generator
* expose the event bridge to be calleable from external 
* use python boto3 to send events to orders event bus
 
## Create EventBridge only

* A simple Event Bridge custom event bus with a target with cloudwatch log group:

```sh
aws cloudformation create-stack --stack-name eventbridge --template-body file://carride-eventbus.yaml
```

* With schema registry
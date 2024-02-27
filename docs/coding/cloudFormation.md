# [AWS CloudFormation](https://docs.aws.amazon.com/cloudformation/index.html)

AWS CloudFormation helps developers to create and manage a collection of related AWS resources as code. The Yaml or JSON template, called a stack, defines AWS resources. Template may be uploaded from a S3 bucket or from our local computer. 

The goal is to repeat infrastructure setup between regions or accounts. Template defines a set of resources that work together to create an application or solution.

Stacks are defined in region, but [StackSets](#stacksets) help to share stacks between accounts and regions.

Stack can be created with other stacks (nested) or common resources can be managed using a separate stack. Nested stacks are not recommended as best practice, as they could be a large area of impact if something goes wrong (all templates will rollback). 

Other stacks can simply refer to the existing resources using cross-stack references. This allows independent teams to be responsible for their resources. When creating a template, developer may indicate what resources are available for cross stack references by exporting those values (Export output field). Other stacks can use `Fn::ImportValue` function to import the value.

To create a stack from AWS templates we can use CLI, API, the Console or start from one of the samples.

The classical steps are:

1. Select a template
1. Prepare any required items for the stack, considering input parameters for example.
1. Create the stack, using CloudFormation console, or AWS [CloudFormation CLI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/cloudformation/index.html#cli-aws-cloudformation) like

    ```sh
    aws cloudformation create-stack --stack-name myteststack --template-body file://sampletemplate.yaml --parameters ParameterKey=KeyPairName,ParameterValue=TestKey
    ```

1. Monitor the stack creation progress
1. Use the stack resources
1. Clean up.

Once stack is created, `Change Sets` may be applied to update the running resources. It is like a summary of the proposed changes. There is also the [`Drift` detection](#drift) feature to identify configuration changes between live resources and template.
It is possible to use a CloudFormation public registry, with 3nd party resources published in APN.

Pay for what the resources use.

## Get started

The infrastructure is defined in Stack. The below example is for an EC2 instance with a user data declaration to install and start Apache webserver, by referencing an existing SSH key pair and security group. See in the folder [labs/CF](https://github.com/jbcodeforce/yarfba/tree/main/labs/CF).

```yaml
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !FindInMap [AWSRegionArch2AMI, !Ref 'AWS::Region', !FindInMap [AWSInstanceType2Arch, !Ref InstanceType, Arch]]      
      InstanceType:
        Ref: t2-micro
      KeyName:
        Ref: my-key-pair
      SecurityGroups:
      - Ref: WebServerSecurityGroup
      UserData:
        Fn::Base64: !Sub |
           #!/bin/bash -xe
           yum update -y
           yum install -y httpd
           systemctl start httpd
           systemctl enable httpd
           EC2-AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)
           echo "<h3>Hello World from $(hostname -f) in AZ= $EC2_AZ </h3>" > /var/www/html/index.html
```

The KeyName property is a literal for an existing key name in the region where the stack is being created.

Use the `Parameters` section to declare values that can be passed to the template when we create the stack.

```yaml
Parameters:      
  KeyName:
    ConstraintDescription: must be the name of an existing EC2 KeyPair.
    Description: Name of an existing EC2 KeyPair to enable SSH access to the instances
    Type: AWS::EC2::KeyPair::KeyName

```

See the [getting started guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/GettingStarted.Walkthrough.html).

* The `Ref` function returns the value of the object it refers to.
* Use `Mappings` to declare conditional values that are evaluated in a similar manner as a look up table statement
* The [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html) function helps to get attribute of a resource.
* Mappings enable us to use an input value as a condition that determines another value. Similar to a switch statement, a mapping associates one set of values with another. Below the ImageId property of the resource Ec2Instance uses the `Fn::FindInMap` function to determine its value by specifying `RegionMap` as the map to use, `AWS::Region` as the input value to map from, and AMI as the label to identify the value to map to.

    ```yaml
    Mappings:
        RegionMap:
            us-east-1:
            AMI: ami-76f0061f
            us-west-1:
            AMI: ami-655a0a20
    Resources:
        Ec2Instance:
            Type: 'AWS::EC2::Instance'
            Properties:
                ImageId: !FindInMap 
                    - RegionMap
                    - !Ref 'AWS::Region'
                    - AMI
    ```

* See [template details](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/gettingstarted.templatebasics.html).
* We can associate the `CreationPolicy` attribute with a resource to prevent its status from reaching create complete until AWS CloudFormation receives a specified number of success signals or the timeout period is exceeded.

Example for S3 bucket and website:

```yaml
Resources:
  HelloBucket:
    Type: 'AWS::S3::Bucket'
    Properties:
      AccessControl: PublicRead
      WebsiteConfiguration:
        IndexDocument: index.html
        ErrorDocument: error.html
```

## StackSets

It is used to create, update, delete stacks across multiple accounts and region in a single operation. An administrator creates the StackSets.

Trusted accounts create, update, delete stack instances from the StackSets. An update to the StackSets, makes all associated stack instances updated.

## Drift

Evaluate all resources that may have changed by admin console, and that will be reversed back to cloud formation template settings.

## Quotas and Limits

There are quotas to consider per account, when authoring templates and creating stacks. 
The relevant product documentation are [AWS CloudFormation endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/cfn.html) and [](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-limits.html).

* The number of stack per account, per region is 2000 as a soft limit.
* StackSet is limited to 1000 per account.

## More advanced topics

### Export resource [from one template to the other](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/walkthrough-crossstackref.html)

Use cross-stack reference, for that define the Export output field to flag the value of a resource output for export. Then, use the Fn::ImportValue intrinsic function to import the value.

Export in Outputs:

```yaml
  "Outputs" : {
    "PublicSubnet" : {
      "Description" : "The subnet ID to use for public web servers",
      "Value" :  { "Ref" : "PublicSubnet" },
      "Export" : { "Name" : {"Fn::Sub": "${AWS::StackName}-SubnetID" }}
    },
```

Reference in another CF template

```yaml
  "Parameters": {
    "NetworkStackName": {
      "Type": "String",
      "Default" : "SampleNetworkCrossStack"
    }
  }
.... 
"NetworkInterfaces" : [{
          "GroupSet"                 : [{ "Fn::ImportValue" :  {"Fn::Sub": "${NetworkStackName}-SecurityGroupID" } }],
          "DeleteOnTermination"      : "true",
          "SubnetId"                 : { "Fn::ImportValue" : {"Fn::Sub": "${NetworkStackName}-SubnetID" } }
```

### Custom resources

[Custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) enable to write custom logic executed on CF creating, updating or deleting a stack. It can run a lambda function to do a lot of thing on an environment. See the [lap-template](https://github.com/jbcodeforce/yarfba/tree/main/labs/security/iam/lab-template.yaml) where a lambda function is called to update a EC2 role or the lambda to update the EC2 for Cloud9.

```yaml
Cloud9SSMRole:
    Type: Custom::Cloud9SSMRole
    Properties:
      ServiceToken: !GetAtt Cloud9SSMRoleFunction.Arn

Cloud9SSMRoleFunction:
    Type: AWS::Lambda::Function
    ...
```



## Deeper dive

* [Introduction from Tutorial Dojo](https://youtu.be/9Xpuprxg7aY)
* [AWS CloudFormation Workshop](https://catalog.workshops.aws/cfn101/en-US) with Git repo [aws-samples/cfn101-workshop](https://github.com/aws-samples/cfn101-workshop) cloned in Code/Studies folder.
* [Best practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)
* [Sample templates for some AWS services](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/sample-templates-services-us-west-1.html)


### Some personal examples

* [EDA workshop cloud formation stack refactorized - lab/eda](https://github.com/jbcodeforce/yarfba/tree/main/labs/eda)

### Tools

* [Use CloudFormation linter](https://github.com/aws-cloudformation/cfn-lint) to validate the yaml declaration
* [Json to Yaml online tool](https://www.json2yaml.com/)
* Consider [CDK](./cdk.md) as a higher abstraction layer to generate Cloud Formation stacks.

## [Service Catalog](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/introduction.html)

Service Catalog is part of a governance practices, within company to define authorized products CF templates. It also support open source Terraform.

It includes a Getting Started Library of well-architected product templates.

Catalog administrator creates a porfolio and then products as CF templates, the user can instantiate. Each portfolio has a IAM permision to access the portfolio for the given users.


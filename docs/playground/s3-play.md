# S3 play with security

This note groups a set of small lab to assess how to use security on top of S3.

In an AWS account, create a user `bob` part of `dev` group, with the following group permissions:

```sh
aws iam create-group --group-name dev
aws iam create-user --user-name bob 
aws iam add-user-to-group --user-name bob --group-name dev
aws iam create-login-profile --user-name bob --password <putalongpassword> --no-password-reset-required
aws iam create-access-key --user-name bob
```

* Attach S3 Full access to the group

```sh
aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --group-name dev
```

* Verify access https://us-west-2.console.aws.amazon.com/console/: using the AWS Account id and `bob` user.
* Create an access key for use bob, using the console or CLI.
* Verify the CLI access with `aws configure` then use profile bob

```sh
aws sts get-caller-identity --profile bob
```

As a developer bob needs to be able to see cloudwatch metrics and logs, so we can add such policies to the dev group.

```sh
aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess --group-name dev
```

## Create S3 bucket


Be sure to get a user with S3 access. 

```sh
export ACCOUNT_ID=
aws s3api create-bucket --bucket bob-data-$ACCOUNT_ID --region us-west-2  \
    --create-bucket-configuration LocationConstraint=us-west-2 --profile bob
```

The bucket is blocked for public access by default, but a `aws s3 cp` will work:

```sh
aws s3 cp ./car-price/Automobile_data.csv s3://bob-data-9...54 --profile bob 
```

* Verify

```sh
aws s3api list-objects --bucket bob-data-9..54 --output text --profile bob
```

[See this git repo for aws s3 and s3api commands](https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/aws-cli/bash-linux/s3/bucket-lifecycle-operations/bucket_operations.sh)

## Create S3 access point

* Define an internet facing access point associate with a unique bucket:

```sh
aws s3control create-access-point --account-id $ACCOUNT_ID --name bob-data-ap \
    --bucket bob-data-$ACCOUNT_ID \
    --public-access-block-configuration BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=true,RestrictPublicBuckets=true \
    --profile bob
# for a VPC specific add
--vpc-configuration VpcI=vpc...
```

* Add policy to get only bob being able to get object.


## Share with pre-signed URL

from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_s3 as s3,
    CfnOutput
)

from constructs import Construct

class CodeWhispererDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
             self, "CWImageQueue",
             queue_name="CWImageQueue",
             visibility_timeout=Duration.seconds(300),
        )

        s3Bucket = s3.Bucket(self, "CWImageBucket",
                        access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                        encryption=s3.BucketEncryption.S3_MANAGED,
                        block_public_access=s3.BlockPublicAccess.BLOCK_ALL)


        imageDB = dynamodb.Table(self, "CWDemoTable",
                                  table_name="CWImageTable",
                                  partition_key=dynamodb.Attribute(name="imageId", type=dynamodb.AttributeType.STRING),
                                  removal_policy=RemovalPolicy.DESTROY
                        )
        
        #imageDB.add_column(dynamodb.Attribute("imageId", dynamodb.AttributeType.STRING))
        #imageDB.add_column(dynamodb.Attribute("labels", dynamodb.AttributeType.ARRAY))

        
        getImageFct = lambda_.Function(self, "GetImageFunction",
                    runtime= lambda_.Runtime.PYTHON_3_10,
                    code=lambda_.Code.from_asset('api/runtime'),
                    handler='get_image.lambda_handler',
                    environment={
                        'BUCKET_NAME': s3Bucket.bucket_name,
                    })
        
        apiGtw = apigw.RestApi(self, "CWdemoApi",
                        rest_api_name="CWDemoApi",
                        deploy_options=apigw.StageOptions(
                            data_trace_enabled=True,
                            metrics_enabled=True,
                            logging_level=apigw.MethodLoggingLevel.INFO,
                            tracing_enabled=True
                        )
                    )
        
        images = apiGtw.root.add_resource('images')
        #images.add_method('GET', handler=getImageFct)
        images.add_method('POST',  apigw.LambdaIntegration(getImageFct))

        # cdk output for api gateway url
        CfnOutput(self, "CWDemoApiUrl", value=apiGtw.url)

        


        

        

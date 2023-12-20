from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda,
    aws_iam as iam,
    aws_ecr,
    # aws_sqs as sqs,
)
from constructs import Construct

class JavaLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        repository= aws_ecr.Repository.from_repository_name(self,"java-lambda-ecr-repo","jbcodeforce/java-lambda")

        sm_role= iam.Role(self,"LambdaRole",
                 assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))
        sm_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        sm_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSXRayDaemonWriteAccess"))
        sm_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
     

        lambdaFct = aws_lambda.DockerImageFunction(self,"JavaLambda",
            code=aws_lambda.DockerImageCode.from_ecr(repository),
            role=sm_role,
            tracing=aws_lambda.Tracing.ACTIVE,
             architecture=aws_lambda.Architecture.ARM_64)


    
       

from aws_cdk import (
    # Duration,
    Stack,  
    aws_iam,
    aws_ec2,
    aws_eks,
    # aws_sqs as sqs,
)
from constructs import Construct

cidr="10.10.0.0/16"

class EksFargateStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # EKS cluster that only uses Fargate capacity
        aws_eks.FargateCluster(self,"MyEKS",
            version=aws_eks.KubernetesVersion.V1_24)
        

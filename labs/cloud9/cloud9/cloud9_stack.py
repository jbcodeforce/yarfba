from aws_cdk import (
    Duration,
    Stack,
    aws_cloud9_alpha as cloud9,
    CfnOutput,
    aws_ec2 as ec2 
)
from constructs import Construct

class Cloud9Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc_name: str = "AcrVPC", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

         # Get existing VPC
        vpc = ec2.Vpc.from_lookup(self, vpc_name, is_default=False)
        print(self.account)
        c9env = cloud9.Ec2Environment(self, "Cloud9Environment",
                                    vpc=vpc, 
                                    description="Jerome's cloud9 env.",
                                    subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                    instance_type=ec2.InstanceType("t3.medium"),
                                    automatic_stop=Duration.hours(1),
                                    ec2_environment_name="Cloud9AcrDemo",
                                    owner=cloud9.Owner.account_root(self.account),
                                    image_id=cloud9.ImageId.AMAZON_LINUX_2)
        CfnOutput(self, "URL", value=c9env.ide_url)
        CfnOutput(self, "EC2_ARN", value=c9env.ec2_environment_arn)
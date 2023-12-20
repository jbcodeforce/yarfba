from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    CfnOutput
)
from constructs import Construct


cidr="10.0.0.0/24"
key_name = "my-ec2-key-pair"
amzn_linux = ec2.MachineImage.latest_amazon_linux(
    generation= ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
    edition= ec2.AmazonLinuxEdition.STANDARD,
    virtualization= ec2.AmazonLinuxVirt.HVM,
    storage= ec2.AmazonLinuxStorage.GENERAL_PURPOSE
)
with open("./user_data/user_data.sh") as f:
    user_data = f.read()

class Ec2Bastion(Construct):
    
    def __init__(self, scope: Stack, construct_id: str, vpcName: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
            
        # Retrieve VPC information
        self.vpc = ec2.Vpc.from_lookup(self, vpcName,
            is_default=True
        )

        # Define a security group 
        self.ec2_security_group = ec2.SecurityGroup(self, "EC2basicSG",
                                                    vpc=self.vpc,
                                                    description="SecurityGroup for EC2 subnet",
                                                    security_group_name="EC2basicSG",
                                                    allow_all_outbound=True,
                                                    )

        self.ec2_security_group.add_ingress_rule(ec2.Peer.ipv4(cidr), ec2.Port.tcp(22), "allow ssh access from the VPC")
        self.instance = ec2.Instance(self, "myKafkaClient",
                                    instance_type= ec2.InstanceType("t2.micro"),
                                    instance_name="myKafkaClient",
                                    machine_image=ec2.MachineImage.latest_amazon_linux(
                                        generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
                                    ),
                                    vpc=self.vpc,
                                    key_name=key_name,
                                    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                    security_group=self.ec2_security_group,
                                    user_data=ec2.UserData.custom(user_data),
                                    )
        
        CfnOutput(self, "EC2_information", value=self.instance.instance_public_ip, description="BastionHost's Public IP")
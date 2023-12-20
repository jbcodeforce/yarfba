from aws_cdk import (
    # Duration,
    Stack,aws_ec2,CfnOutput
    # aws_sqs as sqs,
)
from constructs import Construct

cidr="10.10.0.0/16"
key_name = "my-key-pair"
amzn_linux = aws_ec2.MachineImage.latest_amazon_linux2(
    edition= aws_ec2.AmazonLinuxEdition.STANDARD,
    virtualization= aws_ec2.AmazonLinuxVirt.HVM,
    storage= aws_ec2.AmazonLinuxStorage.GENERAL_PURPOSE
)

with open("./user_data/user_data.sh") as f:
    user_data = f.read()

class Ec2BasicStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Retrieve VPC information
        self.vpc = aws_ec2.Vpc.from_lookup(self, "VPC",
            is_default=True
        )
        # Define a security group 
        self.ec2_security_group = aws_ec2.SecurityGroup(self, "EC2basicSG",
                                                  vpc=self.vpc,
                                                  description="SecurityGroup for EC2 subnet",
                                                  security_group_name="EC2basicSG",
                                                  allow_all_outbound=True,
                                                  )

        #self.ec2_security_group.add_ingress_rule(aws_ec2.Peer.ipv4(cidr), aws_ec2.Port.tcp(22), "allow ssh access from the VPC")
        self.ec2_security_group.add_ingress_rule(aws_ec2.Peer.ipv4(cidr), aws_ec2.Port.tcp(80), "allow HTTP access from the VPC")

        self.instance = aws_ec2.Instance(self, "myHttpdEC2",
                                instance_type= aws_ec2.InstanceType("t2.micro"),
                                instance_name="mySimpleHTTPserver",
                                machine_image=amzn_linux,
                                vpc=self.vpc,
                                key_name=key_name,
                                vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PUBLIC),
                                security_group=self.ec2_security_group,
                                user_data=aws_ec2.UserData.custom(user_data),
                                )
        
        CfnOutput(self, "EC2_information", value=self.instance.instance_public_ip, description="BastionHost's Public IP")
      

from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_logs as logs,
)
from constructs import Construct

CIDR="10.10.0.0/16"
key_name = "my-key-pair"
amzn_linux = ec2.MachineImage.latest_amazon_linux2(
    edition=ec2.AmazonLinuxEdition.STANDARD,
    virtualization=ec2.AmazonLinuxVirt.HVM,
    storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
)

with open("./user_data/user_data.sh") as f:
    user_data = f.read()


class Ec2VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cwLogs = logs.LogGroup(self, '/aws/vpc/flowlogs') 
        self.vpc = ec2.Vpc(self, "VPC",
                           max_azs=2,
                           ip_addresses=ec2.IpAddresses.cidr(CIDR),
                           nat_gateways=2,
                           enable_dns_hostnames=True,
                           enable_dns_support=True,
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   name="public",
                                   subnet_type=ec2.SubnetType.PUBLIC,
                                   cidr_mask=24),
                               ec2.SubnetConfiguration(
                                   subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                                   name="private",
                                   cidr_mask=24) # could be /16 to have more instances, but this is a demo scope.
                           ]
                        )
        self.vpc.add_flow_log("flowlogs",destination=ec2.FlowLogDestination.to_cloud_watch_logs(cwLogs),
                              traftraffic_type=ec2.FlowLogTrafficType.ALL)

        # Create Bastion Host, and authorize SSH to it
        self.bastion = ec2.BastionHostLinux(self, "myBastionHost",
                                            vpc=self.vpc,
                                            subnet_selection=ec2.SubnetSelection(
                                                subnet_type=ec2.SubnetType.PUBLIC),
                                            instance_name="myBastionHostLinux",
                                            instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"))
        self.bastion.instance.instance.add_property_override(
            "KeyName", key_name)

        self.bastion.connections.allow_from_any_ipv4(ec2.Port.tcp(22), "Internet access SSH")

        
        # Define a security group 
        self.ec2_security_group = ec2.SecurityGroup(self, "EC2privateSG",
                                                  vpc=self.vpc,
                                                  description="SecurityGroup for EC2 in private subnet",
                                                  security_group_name="EC2privateSG",
                                                  allow_all_outbound=True,
                                                  )

        self.ec2_security_group.add_ingress_rule(ec2.Peer.ipv4(CIDR), ec2.Port.tcp(22), "allow ssh access from the VPC")
        self.ec2_security_group.add_ingress_rule(ec2.Peer.ipv4(CIDR), ec2.Port.tcp(80), "allow HTTP access from the VPC")

         # EC2 Instance with user data
        self.instance = ec2.Instance(self, "myHttpdEC2",
                                     instance_type=ec2.InstanceType("t2.micro"),
                                     instance_name="mySimpleHTTPserver",
                                     machine_image=amzn_linux,
                                     vpc=self.vpc,
                                     key_name=key_name,
                                     vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                                     security_group=self.ec2_security_group,
                                     user_data=ec2.UserData.custom(user_data),
                                     )

        
        CfnOutput(self, "VPCid", value=self.vpc.vpc_id)
        CfnOutput(self, "BastionHost_information", value=self.bastion.instance_public_ip, description="BastionHost's Public IP")
       

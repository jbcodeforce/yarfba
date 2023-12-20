from aws_cdk import (
    Duration,
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_iam as iam,
    aws_logs as logs,
    # aws_sqs as sqs,
)
from constructs import Construct

CIDR="10.10.0.0/16"
key_name = "my-ec2-key-pair"

amzn_linux = ec2.MachineImage.latest_amazon_linux2(
    edition=ec2.AmazonLinuxEdition.STANDARD,
    virtualization=ec2.AmazonLinuxVirt.HVM,
    storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
)

with open("./user_data/user_data.sh") as f:
    user_data = f.read()

'''
A stack to create a VPC with one public and one private subnet
- Bastion Host in public subnet, It has a predefined role used as instance profile, and a security group for inbound to SSH port
- EC2 in private subnet, with a security group authorizing SSH and port 80 from public subnet.
- S3 bucket without public access
- S3 policy
'''
class Ec2VpceS3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, vpc_name,
                           max_azs=1,
                           ip_addresses=ec2.IpAddresses.cidr(CIDR),
                           vpc_name=vpc_name,
                           nat_gateways=0,
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
        cwLogs = logs.LogGroup(self, '/aws/vpc/flowlogs') 
        self.vpc.add_flow_log("flowlogs",destination=ec2.FlowLogDestination.to_cloud_watch_logs(cwLogs),
                              traftraffic_type=ec2.FlowLogTrafficType.ALL)
        
        # Create Bastion Host, and authorize SSH to it
        self.bastion = ec2.BastionHostLinux(self, "myBastionHost",
                                            vpc=self.vpc,
                                            instance_name="myBastionHostLinux",
                                            machine_image=amzn_linux,
                                            instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"),
                                            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
                                            )


        self.bastion.connections.allow_from_any_ipv4(ec2.Port.tcp(22), "Internet access SSH")
        self.bastion.instance.instance.add_property_override("KeyName", key_name)
        
        # Define a security group 
        self.ec2_security_group = ec2.SecurityGroup(self, "EC2privateSG",
                                                  vpc=self.vpc,
                                                  description="SecurityGroup for EC2 in private subnet",
                                                  security_group_name="EC2privateSG",
                                                  allow_all_outbound=True,
                                                  )

        self.ec2_security_group.add_ingress_rule(ec2.Peer.ipv4(CIDR), ec2.Port.tcp(22), "allow ssh access from the VPC")
        self.ec2_security_group.add_ingress_rule(ec2.Peer.ipv4(CIDR), ec2.Port.tcp(80), "allow HTTP access from the VPC")


        role = iam.Role(self, "Role",
                assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))
        self.instance = ec2.Instance(self, "myHttpdEC2",
                                instance_type= ec2.InstanceType("t2.micro"),
                                instance_name="mySimpleHTTPserver",
                                machine_image=amzn_linux,
                                vpc=self.vpc,
                                role=role,
                                key_name=key_name,
                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                                security_group=self.ec2_security_group,
                                user_data=ec2.UserData.custom(user_data),
                                )

        self.vpc.add_gateway_endpoint("S3Endpoint",
            service=ec2.GatewayVpcEndpointAwsService.S3,
            # Add only to ISOLATED subnets
            subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)]
        )
        
        

        bucket = s3.Bucket(self, "DemoBucket",
                            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                            lifecycle_rules=[
                                s3.LifecycleRule(
                                enabled=True,
                                expiration=Duration.days(365),
                                transitions=[
                                    s3.Transition(
                                    storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                                    transition_after=Duration.days(30)
                                    ),
                                    s3.Transition(
                                    storage_class=s3.StorageClass.GLACIER,
                                    transition_after=Duration.days(90)
                                    ),
                                ]
                                )
                            ]
                        )
        rpolicy = bucket.add_to_resource_policy(
                    iam.PolicyStatement(
                    actions=["s3:GetObject","s3:PutObject"],
                    resources=[bucket.arn_for_objects("file.txt")],
                    principals=[iam.AccountRootPrincipal(),role]
                ))
        CfnOutput(self,"VPC", value=self.vpc.vpc_id, export_name="vpc")
        CfnOutput(self,"Bastion", value=self.bastion.instance_public_ip, export_name="bastion")
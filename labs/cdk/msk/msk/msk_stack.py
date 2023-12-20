from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_msk_alpha as msk,
    aws_iam as iam,
    CfnOutput
)
from constructs import Construct
from msk.ec2_bastion import Ec2Bastion

VPC_NAME="AcrVPC"

class MskStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Get existing VPC

        self.vpc = ec2.Vpc.from_lookup(self, VPC_NAME, is_default=False)
        
        mskSecurityGroup = ec2.SecurityGroup(self, "AcrMSKSecurityGroup",
                                security_group_name="AcrMSKSecurityGroup",
                                vpc=self.vpc,
                                allow_all_outbound=True
                            )

        cluster = msk.Cluster(self, "AcrCluster",
            cluster_name="AcrCluster",
            kafka_version=msk.KafkaVersion.V3_4_0,
            vpc=self.vpc,
            instance_type=ec2.InstanceType("kafka.t3.small"),
            number_of_broker_nodes=1,
            security_groups=[mskSecurityGroup],
            vpc_subnets=ec2.SubnetSelection( subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            ebs_storage_info= msk.EbsStorageInfo(volume_size=10),                         
            client_authentication=msk.ClientAuthentication.sasl(
                iam=True
            )

        )

        taskRole = iam.Role(self, "AcrMSKrole", 
            assumed_by= iam.ServicePrincipal("ec2.amazonaws.com"),
            role_name= "msk-role",
            description= "Role external client can assume to do action on MSK"
        )

        clusterPolicy = iam.Policy(self,"AcrClusterPolicy",
                            statements=[
                               iam.PolicyStatement(
                                effect= iam.Effect.ALLOW,
                                actions=["kafka-cluster:Connect",
                                         "kafka-cluster:DescribeCluster",
                                         "kafka-cluster:DescribeCluster",
                                         "kafka:Get*"],
                                        resources=[cluster.cluster_arn]
                                ),
                                iam.PolicyStatement(
                                effect= iam.Effect.ALLOW,
                                actions=["kafka-cluster:DescribeTopic",
                                    "kafka-cluster:CreateTopic",
                                    "kafka-cluster:WriteData",
                                    "kafka-cluster:ReadData",
                                    "kafka-cluster:AlterGroup",
                                    "kafka-cluster:DescribeGroup"
                                    ],
                                    resources=[cluster.cluster_arn + "/*"]
                                )

                            ])
        taskRole.attach_inline_policy(clusterPolicy)   
        
        CfnOutput(self,"BootstrapServers", value=cluster.bootstrap_brokers)
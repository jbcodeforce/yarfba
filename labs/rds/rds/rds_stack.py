from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    SecretValue,
    RemovalPolicy,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_secretsmanager as asm
)
from constructs import Construct

class RdsAuroraStack(Stack):
    '''
    create a RDS aurora database instance 
    '''
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        db_username = "masteruser"
        db_name = "acrdb"
        db_resource_prefix = f"acr-{self.region}-dev"
        replica_instances = 1
        
        # Get existing VPC
        vpc = ec2.Vpc.from_lookup(self, "AcrVPC", is_default=False)

        ##
        ## Database Security Group
        ##
        allAll = ec2.Port(protocol=ec2.Protocol("ALL"), string_representation="ALL")
        dbsg = ec2.SecurityGroup(self, "DatabaseSecurityGroup",
                vpc = vpc,
                allow_all_outbound = True,
                description = db_resource_prefix + "-SG",
                security_group_name = db_resource_prefix + "-SG",
            )
        dbsg.add_ingress_rule(
            peer =dbsg,
            connection =allAll,
            description="all from self"
            )
        dbsg.add_egress_rule(
            peer =ec2.Peer.ipv4("0.0.0.0/0"),
            connection =allAll,
            description="all out"
            )
        # create a secret for the database
        secret = asm.Secret(self, "DatabaseSecret",
                            description=f"Database secret for {db_resource_prefix}",
                            
                            secret_name=f"{db_resource_prefix}-secret",
                            secret_object_value={
                                "username": SecretValue.unsafe_plain_text(db_username),
                                "password": SecretValue.unsafe_plain_text("passw0rd!"),
                                "dbname": SecretValue.unsafe_plain_text(db_name)
                                },
                            )
        
        cluster = rds.DatabaseCluster(self, "AuroraCluster",
                        engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_15_2),
                        credentials=rds.Credentials.from_secret(secret,username=db_username),
                    
                        deletion_protection=False,
                        serverless_v2_min_capacity=1,
                        serverless_v2_max_capacity=24,
                        instance_props=rds.InstanceProps(
                                instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM),
                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                                vpc=vpc,
                            ),
                            default_database_name=db_name,
                            removal_policy=RemovalPolicy.DESTROY
        )
            
    
        secret= cluster.secret
        CfnOutput(self, "DatabaseUrl",value=cluster.cluster_endpoint.socket_address,export_name=f"{db_resource_prefix}-db-url")
        CfnOutput(self, "DatabaseName",value=db_name)
        CfnOutput(self, "DatabaseUsername",value=db_username)

        
        


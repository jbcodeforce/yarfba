from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    SecretValue
)


class IamUserStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        devGroup=iam.Group.from_group_name(self,"devGroup","developers")
        print(devGroup)
        user = iam.User(self,
                        "Mathieu",
                        user_name="Mathieu",
                        password=SecretValue.unsafe_plain_text("Passw0rd!")
                        )
        user.add_to_group(devGroup)
        '''
        
        role = iam.Role(self,"EC2FullAccess",
                        role_name="EC2FullAccess",
                        description="A role to allow user to do EC2 work",
                        assumed_by=user,
                        managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2FullAccess")])
        '''
from aws_cdk import (
    # Duration,
    Stack,
    Tags,
    SecretValue,
    aws_iam as iam,
    aws_secretsmanager as sm
)
from constructs import Construct

class AbacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # create iam 4 users: one for each project (unicorn and pegaus) and engineering or qas team
        Arnav = iam.User(self, "access-Arnav-peg-eng",user_name="access-Arnav-peg-eng",password=SecretValue.unsafe_plain_text("passw0rd!"), password_reset_required=False)
        Tags.of(Arnav).add("access-project", "peg")
        Tags.of(Arnav).add("access-team", "eng")
        Tags.of(Arnav).add("cost-center", "987654")

        Mary = iam.User(self, "access-Mary-peg-qas",user_name="access-Mary-peg-qas",password=SecretValue.unsafe_plain_text("passw0rd!"), password_reset_required=False)
        Tags.of(Mary).add("access-project", "peg")
        Tags.of(Mary).add("access-team", "qas")
        Tags.of(Mary).add("cost-center", "987654")
        
        Saanvi= iam.User(self,"access-Saanvi-uni-eng",user_name="access-Saanvi-uni-eng",password=SecretValue.unsafe_plain_text("passw0rd!"), password_reset_required=False)
        Tags.of(Saanvi).add("access-project", "uni")
        Tags.of(Saanvi).add("access-team", "eng")
        Tags.of(Saanvi).add("cost-center", "123456")
        
        Carlos = iam.User(self, "access-Carlos-uni-qas",user_name="access-Carlos-uni-qas",password=SecretValue.unsafe_plain_text("passw0rd!"), password_reset_required=False)
        Tags.of(Carlos).add("access-project", "uni")
        Tags.of(Carlos).add("access-team", "qas")
        Tags.of(Carlos).add("cost-center", "123456")

        # Assume any ABAC role, but only when the user and role tags match
        # allows a user to assume any role in the account with the "access-"" role name prefix. 
        # The role must also be tagged with the same project, team, and cost center tags as the user who
        # wants to assume the role
        pstatement= iam.PolicyStatement(
                                      effect=iam.Effect.ALLOW,
                                      resources=["arn:aws:iam::" + self.account +":role/access-*"],
                                      actions=["sts:AssumeRole"],
                                      conditions= {"StringEquals":  {"iam:ResourceTag/access-team": "${aws:PrincipalTag/access-team}"}}
                                      )
        pstatement.add_condition( "StringEquals", {"iam:ResourceTag/access-project": "${aws:PrincipalTag/access-project}"})
        pstatement.add_condition( "StringEquals", {"iam:ResourceTag/cost-center": "${aws:PrincipalTag/cost-center}"})                         
        policy = iam.Policy(self, "policy",
                            policy_name= "access-assume-role",
                            statements= [pstatement],
                            force= True       
                            )
        
       
        # add policy to user (as force = True the policy will be explicite so need to attach to user and not use inline)
        policy.attach_to_user(Arnav)
        policy.attach_to_user(Mary)
        policy.attach_to_user(Saanvi)
        policy.attach_to_user(Carlos)


        # Define policy for role 
        # Allows engineers to read all engineering resources and create and manage Pegasus engineering resources.
        
        
        peg_eng = iam.Role(self, "access-peg-engineering",
                           assumed_by=Arnav,
                           role_name="access-peg-engineering")
        Tags.of(peg_eng).add("access-project", "peg")
        Tags.of(peg_eng).add("access-team", "eng")
        Tags.of(peg_eng).add("cost-center", "987654")
        
        peg_qas = iam.Role(self, "access-peg-quality-assurance",assumed_by=Mary, role_name="access-peg-quality-assurance") 
        Tags.of(peg_qas).add("access-project", "peg")
        Tags.of(peg_qas).add("access-team", "qas")
        Tags.of(peg_qas).add("cost-center", "987654")
        
        uni_dev = iam.Role(self, "access-uni-engineering",
                           assumed_by=Saanvi,
                           role_name="access-uni-engineering") 
        Tags.of(peg_qas).add("access-project", "uni")
        Tags.of(peg_qas).add("access-team", "eng")
        Tags.of(peg_qas).add("cost-center", "123456")

        uni_qas = iam.Role(self, "access-uni-quality-assurance",
                           assumed_by=Carlos,
                           role_name="access-uni-quality-assurance") 
        Tags.of(peg_qas).add("access-project", "uni")
        Tags.of(peg_qas).add("access-team", "qas")
        Tags.of(peg_qas).add("cost-center", "123456")

        statements=[]
        statements.append(iam.PolicyStatement.from_json(
                    {
                        "Sid": "AllActionsSecretsManagerSameProjectSameTeam",
                        "Effect": "Allow",
                        "Action": "secretsmanager:*",
                        "Resource": "*",
                        "Condition": {
                            "StringEquals": {
                                "aws:ResourceTag/access-project": "${aws:PrincipalTag/access-project}",
                                "aws:ResourceTag/access-team": "${aws:PrincipalTag/access-team}",
                                "aws:ResourceTag/cost-center": "${aws:PrincipalTag/cost-center}"
                            },
                            "ForAllValues:StringEquals": {
                                "aws:TagKeys": [
                                    "access-project",
                                    "access-team",
                                    "cost-center",
                                    "Name",
                                    "OwnedBy"
                                ]
                            },
                            "StringEqualsIfExists": {
                                "aws:RequestTag/access-project": "${aws:PrincipalTag/access-project}",
                                "aws:RequestTag/access-team": "${aws:PrincipalTag/access-team}",
                                "aws:RequestTag/cost-center": "${aws:PrincipalTag/cost-center}"
                            }
                        }
                    })
        )
        statements.append(iam.PolicyStatement.from_json({
            "Sid": "AllResourcesSecretsManagerNoTags",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetRandomPassword",
                "secretsmanager:ListSecrets"
            ],
            "Resource": "*"
            })
        )
        statements.append(iam.PolicyStatement.from_json({
            "Sid": "ReadSecretsManagerSameTeam",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:Describe*",
                "secretsmanager:Get*",
                "secretsmanager:List*"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:ResourceTag/access-team": "${aws:PrincipalTag/access-team}"
                }
            }
            })
        )
        statements.append(iam.PolicyStatement.from_json({
            "Sid": "DenyUntagSecretsManagerReservedTags",
            "Effect": "Deny",
            "Action": "secretsmanager:UntagResource",
            "Resource": "*",
            "Condition": {
                "ForAnyValue:StringLike": {
                    "aws:TagKeys": "access-*"
                }
            }
            })
        )
        statements.append(iam.PolicyStatement.from_json({
            "Sid": "DenyPermissionsManagement",
            "Effect": "Deny",
            "Action": "secretsmanager:*Policy",
            "Resource": "*"
            })
        )
        
        
        abac_policy = iam.Policy(self, "abac_policy",
                            policy_name= "access-same-project-team",
                            statements= statements,
                            force= False       
                            )
        
        abac_policy.attach_to_role(peg_eng)
        abac_policy.attach_to_role(peg_qas)
        abac_policy.attach_to_role(uni_dev)
        abac_policy.attach_to_role(uni_qas)

        # Create secrets with the console
        
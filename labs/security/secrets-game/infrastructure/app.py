#!/usr/bin/env python3
import os

import aws_cdk as cdk

from src.fargate_secretsmanager_stack import FargateSecretsManagerStack


app = cdk.App()
env = cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"])
FargateSecretsManagerStack(app, "FargateSecretsmanagerStack",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)

app.synth()

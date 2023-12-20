#!/usr/bin/env python3
import os

import aws_cdk as cdk

from eks_fargate.eks_fargate_stack import EksFargateStack


app = cdk.App()
EksFargateStack(app, "EksFargateStack",

    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)

app.synth()

#!/usr/bin/env python3
import os

import aws_cdk as cdk

from ecs_fargate_flask.ecs_fargate_flask_stack import EcsFargateFlaskStack


app = cdk.App()
EcsFargateFlaskStack(app, "EcsFargateFlaskStack",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    )

app.synth()

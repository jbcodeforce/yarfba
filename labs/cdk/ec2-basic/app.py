#!/usr/bin/env python3
import os

import aws_cdk as cdk

from ec2_basic.ec2_basic_stack import Ec2BasicStack


app = cdk.App()
Ec2BasicStack(app, "Ec2BasicStack",

    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()

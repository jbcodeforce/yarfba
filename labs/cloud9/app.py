#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cloud9.cloud9_stack import Cloud9Stack


app = cdk.App()
Cloud9Stack(app, 
    "Cloud9Stack",
    vpc_name="ArcVPC",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    )

app.synth()

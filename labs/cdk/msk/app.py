#!/usr/bin/env python3
import os

import aws_cdk as cdk

from msk.msk_stack import MskStack




app = cdk.App()
cdkEnv=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
msk=MskStack(app, "MskStack",
        env = cdkEnv
    )

app.synth()

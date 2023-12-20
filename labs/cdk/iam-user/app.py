#!/usr/bin/env python3

import aws_cdk as cdk
import os
from iam_user.iam_user_stack import IamUserStack


app = cdk.App()
IamUserStack(app, "iam-user",
             env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    )

app.synth()

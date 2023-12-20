#!/usr/bin/env python3
import os

import aws_cdk as cdk

from setup.setup_stack import JavaLambdaStack


app = cdk.App()
JavaLambdaStack(app, "JavaLambdaStack",
   
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    )

app.synth()

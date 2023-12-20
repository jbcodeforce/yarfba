#!/usr/bin/env python3
import os

import aws_cdk as cdk

from code_whisperer_demo.code_whisperer_demo_stack import CodeWhispererDemoStack


app = cdk.App()
CodeWhispererDemoStack(app, "CodeWDemoStack",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)

app.synth()

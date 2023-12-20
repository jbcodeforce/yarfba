#!/usr/bin/env python3
import os

import aws_cdk as cdk

from rds.rds_stack import RdsAuroraStack


app = cdk.App()
RdsAuroraStack(app, "RdsAuroraStack",
               env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
               )

app.synth()

#!/usr/bin/env python3
import os

import aws_cdk as cdk

from ec2_vpce_s3.ec2_vpce_s3_stack import Ec2VpceS3Stack


app = cdk.App()
Ec2VpceS3Stack(app, "Ec2VpceS3Stack",vpc_name="Demo",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)

app.synth()

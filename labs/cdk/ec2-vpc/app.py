#!/usr/bin/env python3
import os

import aws_cdk as cdk

from ec2_vpc.ec2_vpc_stack import Ec2VpcStack


app = cdk.App()
Ec2VpcStack(app, "Ec2VpcStack",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    )

app.synth()

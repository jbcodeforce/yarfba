import aws_cdk as core
import aws_cdk.assertions as assertions

from ec2_vpce_s3.ec2_vpce_s3_stack import Ec2VpceS3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in ec2_vpce_s3/ec2_vpce_s3_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Ec2VpceS3Stack(app, "ec2-vpce-s3")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

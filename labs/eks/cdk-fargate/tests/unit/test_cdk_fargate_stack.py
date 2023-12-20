import aws_cdk as core
import aws_cdk.assertions as assertions

from eks_fargate.eks_fargate_stack import EksFargateStack

# example tests. To run these tests, uncomment this file along with the example
# resource in eks_fargate/eks_fargate_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EksFargateStack(app, "cdk-fargate")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

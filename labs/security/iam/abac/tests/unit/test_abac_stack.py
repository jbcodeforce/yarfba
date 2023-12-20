import aws_cdk as core
import aws_cdk.assertions as assertions

from abac.abac_stack import AbacStack

# example tests. To run these tests, uncomment this file along with the example
# resource in abac/abac_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AbacStack(app, "abac")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

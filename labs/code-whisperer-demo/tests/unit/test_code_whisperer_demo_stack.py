import aws_cdk as core
import aws_cdk.assertions as assertions

from code_whisperer_demo.code_whisperer_demo_stack import CodeWhispererDemoStack

# example tests. To run these tests, uncomment this file along with the example
# resource in code_whisperer_demo/code_whisperer_demo_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CodeWhispererDemoStack(app, "code-whisperer-demo")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

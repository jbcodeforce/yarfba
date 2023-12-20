import aws_cdk as core
import aws_cdk.assertions as assertions

from emr_analytics.emr_analytics_stack import EmrAnalyticsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in emr_analytics/emr_analytics_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EmrAnalyticsStack(app, "emr-analytics")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

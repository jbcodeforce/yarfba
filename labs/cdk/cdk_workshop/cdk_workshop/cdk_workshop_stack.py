from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda,
    aws_apigateway as apigw,
)

from .hitcounter import HitCounter
from cdk_dynamo_table_view import TableViewer


class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        my_lambda = aws_lambda.Function(self, 'HelloHandler',
            runtime=aws_lambda .Runtime.PYTHON_3_9,
            code= aws_lambda.Code.from_asset('lambda'),
            handler='hello.handler',
        )

        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=my_lambda,
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_with_counter._handler,
        )

        TableViewer(
            self, 'ViewHitCounter',
            title='Hello Hits',
            table=hello_with_counter.table,
            sort_by='hits'
        )
        

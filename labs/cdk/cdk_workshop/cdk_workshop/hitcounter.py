from constructs import Construct
from aws_cdk import (
    aws_lambda,
    aws_dynamodb as ddb,
    RemovalPolicy
)

class HitCounter(Construct):
    @property
    def handler(self):
        return self._handler 

    @property
    def table(self):
        return self._table

    def __init__(self, scope: Construct, id: str, downstream: aws_lambda.IFunction, **kwargs):
        super().__init__(scope, id, **kwargs)
        # Define a dynamoDB with path as partition key
        self._table = ddb.Table(
            self, 'Hits',
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY
        )

        self._handler = aws_lambda.Function(
            self, 'HitCountHandler',
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler='hitcount.handler',
            code=aws_lambda.Code.from_asset('lambda'),
            environment={
                'DOWNSTREAM_FUNCTION_NAME': downstream.function_name,
                'HITS_TABLE_NAME': self._table.table_name,
            }
        )

        # authorize lambda hitcount to access dynamoDB
        self._table.grant_read_write_data(self._handler)
        # authorize ot to call the downstream lambda
        downstream.grant_invoke(self._handler)
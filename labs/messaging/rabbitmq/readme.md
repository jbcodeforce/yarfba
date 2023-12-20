# Simple getting started with RabbitMQ

## Local test

1. Start RebbitMQ node with docker compose. Use [http://localhost:15672/](http://localhost:15672/) to access RabbitMQ console with guest/guest user.
1. Install pika with: `pip3 install -r requirements.txt`
1. Send basic message: `python3 sender.py`
1. Look at created queues: `docker exec -ti rabbitmq bash -c "rabbitmqctl list_queues"`
1. Start receiver: `python3 receiver.py`

## Remote call to AWS SQS

1. Create SQS cluster and queue with CDK. ()
import pika, os, sys 

# See PIKA API https://pika.readthedocs.io/en/stable/index.html

hostname = os.getenv("mq_host",default = "localhost")
queueName = os.getenv("mq_in_queue",default = "queueA")



def processMessage(channel, method_frame, properties, body):
    print(" [x] Received %r" % body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(hostname))
        channel = connection.channel()
        channel.queue_declare(queue=queueName)
        channel.basic_consume(queue=queueName,
                      auto_ack=False,
                      on_message_callback=processMessage)
        print(' [*] Waiting for messages from {}. To exit press CTRL+C'.format(queueName))
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        channel.stop_consuming()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
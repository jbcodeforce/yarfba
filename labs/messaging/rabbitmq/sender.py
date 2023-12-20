import pika, os

hostname = os.getenv("mq_host",default = "localhost")
queueName = os.getenv("mq_in_queue",default = "queueA")
pid= os.getpid()

connection = pika.BlockingConnection(pika.ConnectionParameters(hostname))

channel = connection.channel()

channel.queue_declare(queue=queueName)
message = "[x] Sent 'Hello World!' from {}".format(pid)
channel.basic_publish(exchange='',
                      routing_key=queueName,
                      body=message)
print(message)
connection.close()
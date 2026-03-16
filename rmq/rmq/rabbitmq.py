import pika 


def publish_message(message):
    params = pika.URLParameters('amqps://basupgjp:YZ2MJHn7tEG3sVsuqMLTYqdZA1hJcNMb@raccoon.lmq.cloudamqp.com/basupgjp') #configure
    connection = pika.BlockingConnection(params) #persistnt connection
    channel = connection.channel() #create channel: virtual connection inside a connection, one connedtion can have multiple channels, each channel can publish/consume messages independently. No need to make mulitple TCP connections for each thread or process. Channels are lightweight and efficient.
    channel.queue_declare("my_queue", durable=True) #declare a queue, if it doesn't exist, it will be created. If it exists, it will be used. Durable means the queue will survive a broker restart. Messages in a durable queue will also survive a broker restart if they are marked as persistent.
    channel.basic_publish(exchange='', routing_key='my_queue', body=message) #publish a message to the queue. Exchange is empty string for default exchange, routing_key is the name of the queue, body is the message to be sent.
    print(f"Message Sent: {message}") 
    connection.close() 


 

#RabbitMQ is mature but has multiple queue types, plugins and all, it can be complex to set up and manage. 
# It is a good choice for complex routing and high availability scenarios. 
# It supports multiple protocols and has a rich set of features, but it can be overkill for simple use cases. 

#LavinMQ is a newer, simpler message broker that is designed to be easy to use and manage.
# It is a good choice for simple use cases and for developers who want a lightweight message broker.
# It has a simpler architecture and fewer features than RabbitMQ, but it is easier to set up and manage.

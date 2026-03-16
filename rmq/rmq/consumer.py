import pika


def callback(ch, method, properties, body):
    print(f"[x] Received: {body.decode()}")


def consume_message():
    params = pika.URLParameters(
        "amqps://basupgjp:YZ2MJHn7tEG3sVsuqMLTYqdZA1hJcNMb@raccoon.lmq.cloudamqp.com/basupgjp"
    )

    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue="my_queue", durable=True)  

    channel.basic_consume(
        queue="my_queue",
        on_message_callback=callback,
        auto_ack=True
    ) #callback function will be called when a message is received. auto_ack means the message will be acknowledged automatically after the callback function is called. If auto_ack is False, you need to call ch.basic_ack(delivery_tag=method.delivery_tag) to acknowledge the message.

    print("Waiting for messages. Press CTRL+C to exit")
    channel.start_consuming()


consume_message() 
#call back function to start consuming messages from the queue. 
# This will block the main thread and keep it running until you stop it manually. 

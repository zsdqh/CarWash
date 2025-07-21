import os
import json
import pika


def send_to_queue(queue_name: str, payload: dict):
    """Отправка JSON-сообщения в очередь RabbitMQ"""
    # Параметры соединения (хост — имя контейнера rabbitmq в вашей сети)
    params = pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'rabbitmq'),
        port=int(os.getenv('RABBITMQ_PORT', 5672)),
        credentials=pika.PlainCredentials(
            os.getenv('RABBITMQ_USERNAME', 'guest'),
            os.getenv('RABBITMQ_PASSWORD', 'guest')
        )
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=body,
        properties=pika.BasicProperties(
            content_type='application/json',
            delivery_mode=2
        )
    )

    connection.close()

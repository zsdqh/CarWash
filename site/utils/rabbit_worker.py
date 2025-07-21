import os
import json
import pika


def send_to_queue(queue_name: str, payload: dict):
    """Отправка JSON-сообщения в очередь RabbitMQ"""
    # Параметры соединения (хост — имя контейнера rabbitmq в вашей сети)
    params = pika.ConnectionParameters(
        host=os.getenv('RABBIT_HOST', 'rabbitmq'),
        port=int(os.getenv('RABBIT_PORT', 5672)),
        credentials=pika.PlainCredentials(
            os.getenv('RABBIT_USER', 'guest'),
            os.getenv('RABBIT_PASS', 'guest')
        )
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Объявление очереди (durable=True для надёжности)
    channel.queue_declare(queue=queue_name, durable=True)

    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=body,
        properties=pika.BasicProperties(
            content_type='application/json',
            delivery_mode=2  # make message persistent
        )
    )

    connection.close()

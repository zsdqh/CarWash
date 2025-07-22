import functools
import os
import json
import asyncio
import aio_pika
from aiogram import Router

from utils.subscriber_worker import SubscriberWorker


async def process_message(message: aio_pika.IncomingMessage, bot):
    async with message.process():
        data = json.loads(message.body.decode('utf-8'))
        text = (
            f"Новая заявка:\n"
            f"Имя: {data['name']}\n"
            f"Телефон: {data['phone']}\n"
            f"Дата: {data['date']}\n"
            "" if not data.get('to_connect') else f"Предпочитаемый способ связи: {data['to_connect']}"
        )
        # Отправляем админу
        sw = SubscriberWorker()
        for sub_id in sw.subs:
            await bot.send_message(chat_id=sub_id, text=text)

import aio_pika
import asyncio

async def connect_with_retry():
    for attempt in range(10):
        try:
            return await aio_pika.connect_robust(
        host=os.getenv('RABBITMQ_HOST', 'rabbitmq'),
        port=int(os.getenv('RABBITMQ_PORT', 5672)),
        login=os.getenv('RABBITMQ_USERNAME', 'guest'),
        password=os.getenv('RABBITMQ_PASSWORD', 'guest')
        )
        except Exception as e:
            await asyncio.sleep(5)

async def rabbitmq_listener(bot):
    # Подключаемся к RabbitMQ
    connection = await connect_with_retry()
    channel = await connection.channel()
    queue = await channel.declare_queue('booking_queue', durable=True)
    # Запускаем потребителя
    await queue.consume(functools.partial(process_message, bot=bot), no_ack=False)

# async def main():
    # Стартуем слушатель в фоне
    # asyncio.create_task(rabbitmq_listener())
    # Запускаем Aiogram-поллинг
    # await dp.start_polling(bot)

# if __name__ == '__main__':
#     asyncio.run(main())

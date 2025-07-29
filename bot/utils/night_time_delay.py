import asyncio
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.subscriber_worker import SubscriberWorker

# Временные рамки ночного периода
start_silent = time(23-3, 0)
end_silent = time(9-3, 0)

# Хранилище отложенных сообщений
delayed_messages = []

# Проверка, находится ли время в "тихом" периоде
def is_silent_time(now: datetime) -> bool:
    current = now.time()
    return current >= start_silent or current < end_silent

# Обработка входящего сообщения
def delay(message: str):
    delayed_messages.append(message)

async def process_delayed(bot):
    sw = SubscriberWorker()
    for sub_id in sw.subs:
        await bot.send_message(chat_id=sub_id, text="🕛Отложенные сообщения:")
    for msg in delayed_messages:
        for sub_id in sw.subs:
            await bot.send_message(chat_id=sub_id, text=msg)
    delayed_messages.clear()
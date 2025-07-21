from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

help_router = Router()
commands = [
    ["/start", "Запуск бота"],
    ["/help", "Информация о командах"],
    ["/subscribe", "Подписаться на рассылку уведомлений"],
    ["/unsubscribe", "Отписаться от рассылки уведомлений"],
    ["/state", "Статус получения уведомлений"],
]


@help_router.message(Command("help"))
async def cmd_start(message: Message):
    await message.answer("\n".join([a[0]+" - "+a[1] for a in commands]))



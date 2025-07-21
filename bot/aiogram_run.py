import asyncio

from aiogram.types import BotCommand
from handlers.help import help_router
from utils.rabbit_worker import rabbitmq_listener
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from handlers.subscribe import subscribe_router
# from work_time.time_func import send_time_msg

async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="help", description="Информация о командах"),
        BotCommand(command="subscribe", description="Подписаться на рассылку уведомлений"),
        BotCommand(command="unsubscribe", description="Отписаться от рассылки уведомлений"),
        BotCommand(command="state", description="Статус получения уведомлений"),
    ]
    await bot.set_my_commands(commands)
    dp.include_router(help_router)
    dp.include_router(start_router)
    dp.include_router(subscribe_router)
    asyncio.create_task(rabbitmq_listener(bot))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
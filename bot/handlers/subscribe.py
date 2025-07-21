from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.dialog_states import DialogStates
from utils.subscriber_worker import SubscriberWorker

subscribe_router = Router()


@subscribe_router.message(Command("subscribe"))
async def subscribe(message: Message, state: FSMContext):
    text = "Введите пароль для подписки"
    await state.set_state(DialogStates.ask_password)
    await message.reply(text)


@subscribe_router.message(Command("state"))
async def state(message):
    sw = SubscriberWorker()
    sub_id = message.from_user.id
    if sw.state(sub_id):
        text = "✅ Вы подписаны на уведомления"
    else:
        text = "❌ Вы не подписаны на уведомления"
    await message.reply(text)

@subscribe_router.message(Command("unsubscribe"))
async def unsubscribe(message: Message):
    sw = SubscriberWorker()
    sub_id = message.from_user.id
    try:
        sw.del_sub(sub_id)
        text = "Вы успешно отписались от уведомлений!"
    except ValueError:
        text = "Вы уже отписаны от уведомления"
    await message.answer(text)


@subscribe_router.message(DialogStates.ask_password)
async def ask_password(message: Message, state: FSMContext):
    sw = SubscriberWorker()
    sub_id = message.from_user.id
    password = message.text

    try:
        sw.add_sub(sub_id, password)
        text = "Вы успешно подписались на уведомления!"
    except ValueError:
        text = "Вы уже подписаны на уведомления"
    except PermissionError:
        text = "Неправильный пароль"
    await state.clear()
    await message.answer(text)

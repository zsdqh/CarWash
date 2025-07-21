from aiogram.fsm.state import StatesGroup, State

class DialogStates(StatesGroup):
    ask_password = State()
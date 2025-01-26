from aiogram.fsm.state import StatesGroup, State


class CheckProductState(StatesGroup):
    wait_articul = State()

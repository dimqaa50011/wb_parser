from aiogram.filters.callback_data import CallbackData


class WBCallbackdata(CallbackData, prefix="wb"):
    check: bool

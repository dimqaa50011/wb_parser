from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callbacdata import WBCallbackdata

markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Посмотреть товар", callback_data=WBCallbackdata(check=True).pack()
            )
        ]
    ]
)

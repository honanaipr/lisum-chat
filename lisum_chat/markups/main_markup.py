from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

estimates_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👍", callback_data="+"),
            InlineKeyboardButton(text="👎", callback_data="-"),
        ]
    ]
)

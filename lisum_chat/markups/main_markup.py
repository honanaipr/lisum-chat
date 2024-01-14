from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

estimates_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👍", callback_data="good"),
            InlineKeyboardButton(text="👎", callback_data="bad"),
        ]
    ]
)

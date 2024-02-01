from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def parce_callback_data(callback_data: str):
    return int(callback_data.split(":")[0]), callback_data.split(":")[1]


def gen_markup(ids: list[int]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for index, id in enumerate(ids, start=1):
        builder.button(text=f"{index}: 👍", callback_data=f"{id}:good")
    builder.button(text="👎", callback_data="bad")
    builder.adjust(2, repeat=True)
    return builder.as_markup()


def patch_markup(
    markup: InlineKeyboardMarkup, id_to_remove: int
) -> InlineKeyboardMarkup | None:
    for row in markup.inline_keyboard:
        for button in row:
            if (
                button.callback_data
                and not button.callback_data == "bad"
                and parce_callback_data(button.callback_data)[0] == id_to_remove
            ):
                row.remove(button)
    has_buttons = False
    for row in markup.inline_keyboard:
        for button in row:
            if button.callback_data and not button.callback_data == "bad":
                has_buttons = True
    if not has_buttons:
        return None
    return markup

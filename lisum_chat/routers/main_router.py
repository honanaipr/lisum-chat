from aiogram import Router, types, F
from .. import redmine
from ..markups.main_markup import estimates_markup

main_router = Router()


@main_router.message(F.text.as_("message_text"))
async def message_handler(message: types.Message, message_text: str) -> None:
    result_message = await message.answer("⏳✍")
    try:
        search_result = [
            result.url for result in (await redmine.search(message_text)).results[:3]
        ]
        search_result = "\n".join(search_result)
        assert search_result
    except Exception as e:
        await result_message.edit_text(f"❗️ Ошибка\n{e}", parse_mode=None)
        print(e)
    else:
        await result_message.edit_text(
            search_result, parse_mode=None, reply_markup=estimates_markup
        )


@main_router.callback_query()
async def my_callback_foo(query: types.CallbackQuery):
    print(query.data)
    if isinstance(query.message, types.Message):
        await query.message.edit_reply_markup(reply_markup=None)
    if query.data == "+":
        await query.answer(text="👍", show_alert=False)
    if query.data == "-":
        await query.answer(text="👎", show_alert=False)

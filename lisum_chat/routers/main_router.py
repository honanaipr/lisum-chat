from aiogram import Router, types, F
from .. import redmine

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
        await result_message.edit_text(search_result, parse_mode=None)

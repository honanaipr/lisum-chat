from aiogram import Router, types, F
from .. import redmine

main_router = Router()


@main_router.message(F.text.as_("message_text"))
async def message_handler(message: types.Message, message_text: str) -> None:
    result_message = await message.answer("⏳✍")
    search_result = (await redmine.search(message_text)).results[0].model_dump_json()
    await result_message.edit_text(search_result, parse_mode=None)

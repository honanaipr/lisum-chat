from aiogram import Router, types, F
from .. import redmine
from ..markups.main_markup import estimates_markup
from ..database import SessionLocal
from ..crud.estimate_crud import add_estimate, add_response
from typing import Literal

main_router = Router()


@main_router.message(F.text.as_("message_text"))
async def message_handler(message: types.Message, message_text: str) -> None:
    result_message = await message.reply("⏳✍")
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
        try:
            with SessionLocal() as session:
                add_response(
                    session=session,
                    query_text=message_text,
                    responce_text=search_result,
                    message_id=message.message_id,
                    chat_id=message.chat.id,
                )
                session.commit()
        except Exception as e:
            await result_message.edit_text(f"❗️ Ошибка\n{e}", parse_mode=None)
            print(e)
        else:
            await result_message.edit_text(
                search_result, parse_mode=None, reply_markup=estimates_markup
            )


@main_router.callback_query(
    F.message.chat.id.as_("chat_id"),
    F.message.reply_to_message.message_id.as_("original_message_id"),
    F.data.in_(["good", "bad"]),
    F.data.as_("query_data"),
)
async def my_callback_foo(
    query: types.CallbackQuery,
    chat_id: int,
    original_message_id: int,
    query_data: Literal["good", "bad"],
):
    if isinstance(query.message, types.Message):
        await query.message.edit_reply_markup(reply_markup=None)
    else:
        return
    with SessionLocal() as session:
        add_estimate(
            session=session,
            chat_id=chat_id,
            message_id=original_message_id,
            estimate=query_data,
        )
        session.commit()
    if query_data == "good":
        await query.answer(text="👍", show_alert=False)
    else:
        await query.answer(text="👎", show_alert=False)

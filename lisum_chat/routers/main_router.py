from aiogram import Router, types, F
from .. import redmine
from ..markups.main_markup import estimates_markup
from ..database import SessionLocal
from ..crud.estimate_crud import add_estimate, add_response, add_query
from typing import Literal
from aiogram.filters import Filter
from ..bot import bot

main_router = Router()


class ReplyToMeFilter(Filter):
    async def __call__(self, message: types.Message) -> bool | dict[str, int]:
        reply_to_user_id = F.reply_to_message.from_user.id.resolve(message)
        original_message_id = F.reply_to_message.reply_to_message.message_id.resolve(
            message
        )
        if reply_to_user_id and reply_to_user_id == (await bot.me()).id:
            return {"original_message_id": original_message_id}
        return False


@main_router.message(ReplyToMeFilter())
async def reply_message_handler(
    message: types.Message, original_message_id: int
) -> None:
    print(original_message_id)


@main_router.message(F.text.as_("message_text"))
async def query_handler(message: types.Message, message_text: str) -> None:
    result_message = await message.reply("⏳✍")
    try:
        results_list = [
            result.url for result in (await redmine.search(message_text)).results[:3]
        ]
        search_result = "\n".join(results_list)
        assert search_result
    except Exception as e:
        await result_message.edit_text(f"❗️ Ошибка\n{e}", parse_mode=None)
        print(e)
    else:
        try:
            with SessionLocal() as session:
                add_query(
                    session=session,
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    query_text=message_text,
                )
                session.commit()
                for result in results_list:
                    add_response(
                        session=session,
                        query_message_id=message.message_id,
                        response_text=result,
                        message_id=result_message.message_id,
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
    F.message.message_id.as_("response_message_id"),
    F.data.in_(["good", "bad"]),
    F.data.as_("query_data"),
)
async def my_callback_foo(
    query: types.CallbackQuery,
    chat_id: int,
    response_message_id: int,
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
            query_id=query.id,
            estimate=query_data,
            response_message_id=response_message_id,
        )
        session.commit()
    if query_data == "good":
        await query.answer(text="👍", show_alert=False)
    else:
        await query.answer(text="👎", show_alert=False)

from aiogram import Router, types, F
from .. import redmine
from ..markups.main_markup import gen_markup, parce_callback_data, patch_markup
from ..database import SessionLocal
from ..crud.estimate_crud import (
    add_estimate,
    add_response,
    add_query,
    add_enhancement,
    get_responses_by_message_id,
)
from aiogram.filters import Filter
from ..bot import bot

main_router = Router()


class ReplyToMeFilter(Filter):
    async def __call__(self, message: types.Message) -> bool | dict[str, int]:
        reply_to_user_id = F.reply_to_message.from_user.id.resolve(message)
        origin_message_id = F.reply_to_message.message_id.resolve(message)
        if reply_to_user_id and reply_to_user_id == (await bot.me()).id:
            return {"origin_message_id": origin_message_id}
        return False


@main_router.message(ReplyToMeFilter(), F.text.as_("message_text"))
async def reply_message_handler(
    message: types.Message, origin_message_id: int, message_text: str
) -> None:
    with SessionLocal() as session:
        add_enhancement(
            session=session,
            message_id=message.message_id,
            chat_id=message.chat.id,
            enhancement_text=message_text,
            response_message_id=origin_message_id,
        )
        session.commit()


@main_router.message(F.text.as_("message_text"))
async def query_handler(message: types.Message, message_text: str) -> None:
    result_message = await message.reply("⏳✍")
    try:
        results = (await redmine.search(message_text)).results[:3]
        response_text = "\n\n".join(
            [
                f"{index}: {result.title}\n{result.url} "
                for index, result in enumerate(results, start=1)
            ]
        )
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
                if not results:
                    await result_message.edit_text(
                        "❗️ Ничего не найдено :(", parse_mode=None
                    )
                    return
                response_ids = []
                for result in results:
                    response_id = add_response(
                        session=session,
                        query_message_id=message.message_id,
                        response_text=result.url,
                        message_id=result_message.message_id,
                        chat_id=message.chat.id,
                    )
                    response_ids.append(response_id)
                session.commit()
        except Exception as e:
            await result_message.edit_text(f"❗️ Ошибка\n{e}", parse_mode=None)
            print(e)
        else:
            await result_message.edit_text(
                response_text, parse_mode=None, reply_markup=gen_markup(response_ids)
            )


@main_router.callback_query(
    F.message.chat.id.as_("chat_id"),
    F.message.message_id.as_("response_message_id"),
    # F.data.in_(["good", "bad"]),
    F.data.as_("query_data"),
)
async def my_callback_foo(
    query: types.CallbackQuery,
    chat_id: int,
    response_message_id: int,
    query_data: str,
):
    if query_data == "bad":
        if isinstance(query.message, types.Message):
            await query.message.edit_reply_markup(reply_markup=None)
        with SessionLocal() as session:
            for responce_id in get_responses_by_message_id(
                message_id=response_message_id, chat_id=chat_id, session=session
            ):
                add_estimate(
                    session=session,
                    chat_id=chat_id,
                    query_id=query.id,
                    estimate=query_data,
                    response_id=responce_id,
                )
            session.commit()
    else:
        responce_id, estimate = parce_callback_data(query_data)
        if isinstance(query.message, types.Message) and query.message.reply_markup:
            patched_markup = patch_markup(query.message.reply_markup, responce_id)
            await query.message.edit_reply_markup(reply_markup=patched_markup)
        with SessionLocal() as session:
            add_estimate(
                session=session,
                chat_id=chat_id,
                query_id=query.id,
                estimate=estimate,
                response_id=responce_id,
            )
            session.commit()
    if query_data == "good":
        await query.answer(text="👍", show_alert=False)
    else:
        await query.answer(text="👎", show_alert=False)

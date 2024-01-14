from ..models.estimates_model import Estimate
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Literal


def add_response(
    session: Session,
    query_text: str,
    responce_text: str,
    message_id: int,
    chat_id: int,
):
    db_estimate = Estimate(
        query_text=query_text,
        responce_text=responce_text,
        responce_message_id=message_id,
        responce_chat_id=chat_id,
    )
    session.add(db_estimate)


def add_estimate(
    session: Session, chat_id: int, message_id: int, estimate: Literal["good", "bad"]
):
    stmt = (
        select(Estimate)
        .where(Estimate.responce_chat_id == chat_id)
        .where(Estimate.responce_message_id == message_id)
    )
    db_estimate = session.scalars(stmt).one()
    db_estimate.estimate = estimate

from ..models.response_model import Response
from ..models.query_model import Query
from ..models.estimate_model import Estimate
from ..models.enhancement_model import Enhancement
from sqlalchemy.orm import Session
from sqlalchemy import select


def add_query(
    session: Session,
    query_text: str,
    message_id: int,
    chat_id: int,
):
    db_estimate = Query(
        query_text=query_text,
        message_id=message_id,
        chat_id=chat_id,
    )
    session.add(db_estimate)
    session.flush()
    return db_estimate.id


def add_response(
    session: Session,
    response_text: str,
    query_message_id: int,
    message_id: int,
    chat_id: int,
):
    stmt = (
        select(Query)
        .where(Query.message_id == query_message_id)
        .where(Query.chat_id == chat_id)
    )
    db_query = session.scalars(stmt).one()
    db_estimate = Response(
        query_id=db_query.id,
        response_text=response_text,
        message_id=message_id,
        chat_id=chat_id,
    )
    session.add(db_estimate)
    session.flush()
    return db_estimate.id


def add_estimate(
    session: Session,
    chat_id: int,
    query_id: str,
    estimate: str,
    response_id: int,
):
    stmt = select(Response).where(Response.id == response_id)
    db_response = session.scalars(stmt).one()
    db_estimate = Estimate(
        response_id=db_response.id,
        estimate=estimate,
        query_id=query_id,
        chat_id=chat_id,
    )
    session.add(db_estimate)
    session.flush()
    return db_estimate.id


def add_enhancement(
    session: Session,
    chat_id: int,
    message_id: int,
    enhancement_text: str,
    response_message_id: int,
):
    stmt = (
        select(Response)
        .where(Response.chat_id == chat_id)
        .where(Response.message_id == response_message_id)
    )
    db_response = session.scalars(stmt).first()
    if db_response is None:
        raise Exception("Response not found!")
    db_enhancement = Enhancement(
        query_id=db_response.query.id,
        enhancement_text=enhancement_text,
        message_id=message_id,
        chat_id=chat_id,
    )
    session.add(db_enhancement)
    session.flush()
    return db_enhancement.id


def get_responses_by_message_id(
    session: Session, chat_id: int, message_id
) -> list[int]:
    stmt = (
        select(Response)
        .where(Response.chat_id == chat_id)
        .where(Response.message_id == message_id)
    )
    db_responses = session.scalars(stmt)
    return [db_response.id for db_response in db_responses]

from ..models.estimates_model import Estimate
from sqlalchemy.orm import Session


def add_estimate(session: Session, reply: str, estimate: bool):
    db_estimate = Estimate(reply=reply, estimate=estimate)
    session.add(db_estimate)

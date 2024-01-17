from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class Estimate(Base):
    __tablename__ = "estimate"
    id: Mapped[int] = mapped_column(primary_key=True)
    response_id: Mapped[int] = mapped_column(ForeignKey("response.id"))
    query_id: Mapped[str]
    chat_id: Mapped[int]
    estimate: Mapped[str]

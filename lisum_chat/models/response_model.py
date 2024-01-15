from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class Response(Base):
    __tablename__ = "response"
    id: Mapped[int] = mapped_column(primary_key=True)
    query_id: Mapped[int] = mapped_column(ForeignKey("query.id"))
    message_id: Mapped[int]
    chat_id: Mapped[int]
    response_text: Mapped[str]
    response_url: Mapped[str | None]

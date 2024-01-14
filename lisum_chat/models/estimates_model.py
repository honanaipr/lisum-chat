from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Literal
from sqlalchemy.dialects.sqlite.json import JSON


class Estimate(Base):
    __tablename__ = "estimate"
    id: Mapped[int] = mapped_column(primary_key=True)
    responce_message_id: Mapped[int]
    responce_chat_id: Mapped[int]
    query_text: Mapped[str]
    responce_text: Mapped[str]
    responce_urls: Mapped[list[str] | None] = mapped_column(JSON, default=[])
    enhancement_text: Mapped[str] = mapped_column(default="")
    enhancement_urls: Mapped[list[str]] = mapped_column(JSON, default=[])
    estimate: Mapped[Literal["good", "bad"] | None] = mapped_column(default=None)

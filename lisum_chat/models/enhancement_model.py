from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class Enhancement(Base):
    __tablename__ = "enhancement"
    id: Mapped[int] = mapped_column(primary_key=True)
    response_id: Mapped[int] = mapped_column(ForeignKey("response.id"))
    message_id: Mapped[int]
    chat_id: Mapped[int]
    enhancement_text: Mapped[str]
    enhancement_url: Mapped[str | None]

from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Query(Base):
    __tablename__ = "query"
    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int]
    chat_id: Mapped[int]
    query_text: Mapped[str]

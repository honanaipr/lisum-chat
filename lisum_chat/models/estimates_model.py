from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Estimate(Base):
    __tablename__ = "estimate"
    id: Mapped[int] = mapped_column(primary_key=True)
    reply: Mapped[str]
    estimate: Mapped[bool]

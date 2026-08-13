from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ItemDefinition(Base):
    __tablename__ = "item_definitions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=False,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    localization_key: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    stackable: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    max_stack: Mapped[int] = mapped_column(
        Integer,
        default=999,
        nullable=False,
    )
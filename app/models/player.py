import uuid

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    display_name: Mapped[str] = mapped_column(String(32), nullable=False)

    level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    experience: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    coins: Mapped[int] = mapped_column(Integer, default=100, nullable=False)

    energy: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    max_energy: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    starter_pack_granted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )




    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    last_active_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    identities = relationship(
        "PlayerIdentity",
        back_populates="player",
        cascade="all, delete-orphan",
    )



    inventory_items = relationship(
        "InventoryItem",
        back_populates="player",
        cascade="all, delete-orphan",
    )





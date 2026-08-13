import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    __table_args__ = (
        UniqueConstraint(
            "player_id",
            "item_id",
            name="uq_inventory_player_item",
        ),
        CheckConstraint(
            "quantity >= 0",
            name="ck_inventory_quantity_nonnegative",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    player_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("players.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    item_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("item_definitions.id"),
        nullable=False,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    player = relationship(
        "Player",
        back_populates="inventory_items",
    )

    definition = relationship("ItemDefinition")
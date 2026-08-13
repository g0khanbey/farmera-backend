from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_player
from app.db.session import get_db
from app.models.inventory_item import InventoryItem
from app.models.item_definition import ItemDefinition
from app.models.player import Player
from app.schemas.inventory import (
    InventoryItemResponse,
    InventoryResponse,
)


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.get(
    "/me",
    response_model=InventoryResponse,
    status_code=status.HTTP_200_OK,
)
def get_my_inventory(
    player: Player = Depends(get_current_player),
    db: Session = Depends(get_db),
) -> InventoryResponse:
    rows = db.execute(
        select(
            InventoryItem.item_id,
            ItemDefinition.code,
            ItemDefinition.localization_key,
            ItemDefinition.category,
            InventoryItem.quantity,
            ItemDefinition.stackable,
            ItemDefinition.max_stack,
        )
        .join(
            ItemDefinition,
            ItemDefinition.id == InventoryItem.item_id,
        )
        .where(
            InventoryItem.player_id == player.id,
            InventoryItem.quantity > 0,
        )
        .order_by(InventoryItem.item_id)
    ).all()

    items = [
        InventoryItemResponse(
            item_id=row.item_id,
            code=row.code,
            localization_key=row.localization_key,
            category=row.category,
            quantity=row.quantity,
            stackable=row.stackable,
            max_stack=row.max_stack,
        )
        for row in rows
    ]

    return InventoryResponse(items=items)
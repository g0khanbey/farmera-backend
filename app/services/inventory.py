from typing import Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory_item import InventoryItem
from app.models.item_definition import ItemDefinition
from app.models.player import Player


ITEM_DEFINITIONS = [
    {
        "id": 1001,
        "code": "carrot",
        "localization_key": "item.carrot.name",
        "category": "crop",
        "stackable": True,
        "max_stack": 999,
    },
    {
        "id": 2001,
        "code": "wooden_hoe",
        "localization_key": "item.wooden_hoe.name",
        "category": "tool",
        "stackable": False,
        "max_stack": 1,
    },
    {
        "id": 2002,
        "code": "wooden_watering_can",
        "localization_key": "item.wooden_watering_can.name",
        "category": "tool",
        "stackable": False,
        "max_stack": 1,
    },
]

STARTER_ITEMS: Dict[int, int] = {
    1001: 4,
    2001: 1,
    2002: 1,
}


def create_item_definitions_if_missing(db: Session) -> None:
    for definition_data in ITEM_DEFINITIONS:
        definition = db.get(
            ItemDefinition,
            definition_data["id"],
        )

        if definition is None:
            db.add(ItemDefinition(**definition_data))

    db.flush()


def grant_starter_pack_if_needed(
    db: Session,
    player: Player,
) -> bool:
    if player.starter_pack_granted:
        return False

    create_item_definitions_if_missing(db)

    for item_id, quantity in STARTER_ITEMS.items():
        inventory_item = db.scalar(
            select(InventoryItem).where(
                InventoryItem.player_id == player.id,
                InventoryItem.item_id == item_id,
            )
        )

        if inventory_item is None:
            db.add(
                InventoryItem(
                    player_id=player.id,
                    item_id=item_id,
                    quantity=quantity,
                )
            )
        else:
            inventory_item.quantity += quantity

    player.starter_pack_granted = True
    db.flush()

    return True
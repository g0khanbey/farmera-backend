from typing import List

from pydantic import BaseModel


class InventoryItemResponse(BaseModel):
    item_id: int
    code: str
    localization_key: str
    category: str
    quantity: int
    stackable: bool
    max_stack: int


class InventoryResponse(BaseModel):
    items: List[InventoryItemResponse]
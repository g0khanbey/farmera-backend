from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_current_player
from app.models.player import Player
from app.schemas.auth import PlayerResponse


router = APIRouter(
    prefix="/players",
    tags=["Players"],
)


@router.get(
    "/me",
    response_model=PlayerResponse,
    status_code=status.HTTP_200_OK,
)
def get_me(
    player: Player = Depends(get_current_player),
) -> PlayerResponse:
    return PlayerResponse.model_validate(player)
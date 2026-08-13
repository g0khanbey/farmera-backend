from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import (
    GoogleCodeLoginRequest,
    GoogleLoginRequest,
    LoginResponse,
    PlayerResponse,
)
from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.auth import (
    GoogleLoginRequest,
    LoginResponse,
    PlayerResponse,
)
from app.services.auth import (
    login_or_create_google_player,
    login_or_create_google_player_from_code,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/google",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
def google_login(
    request: GoogleLoginRequest,
    db: Session = Depends(get_db),
) -> LoginResponse:
    try:
        player, is_new_player = login_or_create_google_player(
            db,
            request.id_token,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    access_token, expires_in = create_access_token(player.id)

    return LoginResponse(
        access_token=access_token,
        expires_in=expires_in,
        is_new_player=is_new_player,
        player=PlayerResponse.model_validate(player),
    )


@router.post(
    "/google/code",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
def google_code_login(
    request: GoogleCodeLoginRequest,
    db: Session = Depends(get_db),
) -> LoginResponse:
    try:
        player, is_new_player = (
            login_or_create_google_player_from_code(
                db=db,
                code=request.code,
                code_verifier=request.code_verifier,
                redirect_uri=request.redirect_uri,
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    access_token, expires_in = create_access_token(player.id)

    return LoginResponse(
        access_token=access_token,
        expires_in=expires_in,
        is_new_player=is_new_player,
        player=PlayerResponse.model_validate(player),
    )









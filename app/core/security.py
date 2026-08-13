import uuid
from datetime import datetime, timedelta, timezone
from typing import Tuple

import jwt
from jwt import InvalidTokenError

from app.core.config import settings


ALGORITHM = "HS256"


def create_access_token(player_id: uuid.UUID) -> Tuple[str, int]:
    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(player_id),
        "type": "access",
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=ALGORITHM,
    )

    return token, expires_in


def decode_access_token(token: str) -> uuid.UUID:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[ALGORITHM],
        )
    except InvalidTokenError as exc:
        raise ValueError("Gecersiz veya suresi dolmus oturum") from exc

    if payload.get("type") != "access":
        raise ValueError("Gecersiz token turu")

    player_id = payload.get("sub")

    if not player_id:
        raise ValueError("Token oyuncu kimligi icermiyor")

    try:
        return uuid.UUID(player_id)
    except ValueError as exc:
        raise ValueError("Gecersiz oyuncu kimligi") from exc
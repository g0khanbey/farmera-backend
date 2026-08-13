from datetime import datetime, timezone
from typing import Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.player import Player
from app.models.player_identity import PlayerIdentity
from app.services.google_auth import (
    exchange_google_code,
    verify_google_id_token,
)


def login_or_create_google_player(
    db: Session,
    google_token: str,
) -> Tuple[Player, bool]:
    profile = verify_google_id_token(google_token)

    identity = db.scalar(
        select(PlayerIdentity).where(
            PlayerIdentity.provider == "google",
            PlayerIdentity.provider_subject == profile.subject,
        )
    )

    now = datetime.now(timezone.utc)

    if identity is not None:
        identity.email = profile.email
        identity.email_verified = profile.email_verified
        identity.profile_picture_url = profile.picture
        identity.last_login_at = now
        identity.player.last_active_at = now

        try:
            db.commit()
            db.refresh(identity.player)
        except Exception:
            db.rollback()
            raise

        return identity.player, False

    display_name = (profile.name or profile.email.split("@")[0]).strip()

    if not display_name:
        display_name = "Farmer"

    player = Player(
        display_name=display_name[:32],
    )

    identity = PlayerIdentity(
        player=player,
        provider="google",
        provider_subject=profile.subject,
        email=profile.email,
        email_verified=profile.email_verified,
        profile_picture_url=profile.picture,
        last_login_at=now,
    )

    db.add(player)
    db.add(identity)

    try:
        db.commit()
        db.refresh(player)
    except Exception:
        db.rollback()
        raise

    return player, True

def login_or_create_google_player_from_code(
    db: Session,
    code: str,
    code_verifier: str,
    redirect_uri: str,
) -> Tuple[Player, bool]:
    google_token = exchange_google_code(
        code=code,
        code_verifier=code_verifier,
        redirect_uri=redirect_uri,
    )

    return login_or_create_google_player(
        db=db,
        google_token=google_token,
    )









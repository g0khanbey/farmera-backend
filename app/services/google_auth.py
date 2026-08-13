from dataclasses import dataclass
from typing import Optional

from google.auth.transport import requests
from google.oauth2 import id_token

from app.core.config import settings


@dataclass(frozen=True)
class GoogleProfile:
    subject: str
    email: str
    email_verified: bool
    name: Optional[str]
    picture: Optional[str]


def verify_google_id_token(token: str) -> GoogleProfile:
    try:
        payload = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
    except ValueError as exc:
        raise ValueError("Gecersiz Google ID token") from exc

    subject = payload.get("sub")
    email = payload.get("email")
    email_verified = payload.get("email_verified") is True

    if not subject:
        raise ValueError("Google kullanici kimligi bulunamadi")

    if not email or not email_verified:
        raise ValueError("Dogrulanmis Google e-postasi bulunamadi")

    return GoogleProfile(
        subject=subject,
        email=email,
        email_verified=email_verified,
        name=payload.get("name"),
        picture=payload.get("picture"),
    )
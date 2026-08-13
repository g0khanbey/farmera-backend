from dataclasses import dataclass
from typing import Optional
import requests as http_requests
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
def exchange_google_code(
    code: str,
    code_verifier: str,
    redirect_uri: str,
) -> str:
    allowed_redirect_uri = "http://127.0.0.1:53682/"

    if redirect_uri != allowed_redirect_uri:
        raise ValueError("Gecersiz Google yonlendirme adresi")

    try:
        response = http_requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "code_verifier": code_verifier,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
            timeout=15,
        )
    except http_requests.RequestException as exc:
        raise ValueError(
            "Google token servisine ulasilamadi"
        ) from exc

    try:
        response_data = response.json()
    except ValueError as exc:
        raise ValueError(
            "Google token servisi gecersiz cevap verdi"
        ) from exc

    if not response.ok:
        error_description = response_data.get(
            "error_description",
            "Google kodu tokena cevrilemedi",
        )
        raise ValueError(error_description)

    google_id_token = response_data.get("id_token")

    if not google_id_token:
        raise ValueError("Google ID token dondurmedi")

    return google_id_token





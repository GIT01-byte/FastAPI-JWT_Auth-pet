from datetime import timedelta

from config import settings

from schemas.users import UserInDB

from utils.security import encode_jwt


TOKEN_TYPE_FIELD = 'type'
ACCESS_TOKEN_TYPE = 'access_token'
REFRESH_TOKEN_TYPE = 'refresh_token'


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.jwt_auth.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {
        TOKEN_TYPE_FIELD: token_type,
    }
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
        )


def create_access_token(user_id: str) -> str:
    jwt_payload = {
        'sub': user_id,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.jwt_auth.access_token_expire_minutes,
    )

def create_refresh_token(user_id: str) -> str:
    jwt_payload = {
        'sub': user_id,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.jwt_auth.refresh_token_expire_days),
    )

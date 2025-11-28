import bcrypt

from datetime import timedelta, datetime, timezone

import jwt

from config import settings


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

def check_password(
    password: str,
    password_hash: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=password_hash,
    )


def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt_auth.private_key_path.read_text(),
    algorithm: str = settings.jwt_auth.algorithm,
    expire_minutes: int = settings.jwt_auth.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )
    return encoded

def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt_auth.public_key_path.read_text(),
    algorithm: str = settings.jwt_auth.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm]
    )
    return decoded

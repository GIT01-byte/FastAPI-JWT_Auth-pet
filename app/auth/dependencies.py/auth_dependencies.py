from jwt import InvalidTokenError

from fastapi import (
    Depends, 
    Form, 
    HTTPException, 
    status,
    )

from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
    )

from app.auth.schemas.users import UserInDB
from utils.security import check_password, decode_jwt
from db.user_repository import UsersRepo

from services.jwt_tokens import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE
    )


http_bearer = HTTPBearer(auto_error=False)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/jwt_auth/login/'
    )


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid username or password'
    )
    user = await UsersRepo.select_user_by_username(username)
    
    if not user:
        raise unauthed_exp
    
    if not check_password(
        password=password,
        password_hash=user.password_hash,
    ):
        raise unauthed_exp
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user inactive'
        )
    
    return user


def get_current_token_payload(
    token: str = Depends(oauth2_scheme)
) -> UserSchema:
    try:
        payload = decode_jwt(
        token=token,
    )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'invalid token error: {e}'
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid token type: {current_token_type!r} expected: {token_type!r}'
        )

def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str | None = payload.get('sub')
    if user:= users_db.get(username):  # type: ignore
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='token invalid (user not found)'
    )

def get_auth_user_from_token_of_type(token_type: str):
    def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload)
    ) -> UserSchema:
        validate_token_type(payload, token_type)
        return get_user_by_token_sub(payload)
    return get_auth_user_from_token


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)

get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user)
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='User inactive', 
    )

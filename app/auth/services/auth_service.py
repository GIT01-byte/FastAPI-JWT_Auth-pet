from services.jwt_tokens import (
    create_access_token,
    create_refresh_token,
    )

from exceptions.exceptions import (
    InvalidCredentialsError,
    InvalidPasswordError,
    PasswordRequiredError,
    UserNotFoundError,
    UserInactiveError,
    )

from utils.security import check_password
from db.user_repository import UsersRepo



async def authenticate_user(username: str, password: str):
    user = await UsersRepo.select_user_by_username(username)

    if not user:
        raise UserNotFoundError()
    
    if not check_password(
        password=password,
        password_hash=user.password_hash
        ):
        raise InvalidPasswordError()
    
    if not user.is_active:
        raise UserInactiveError()

    # Генерируем токены
    user_id = user.id
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return {
        "user_id": user_id,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

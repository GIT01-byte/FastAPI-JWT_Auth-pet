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

from exceptions.exceptions import (
    InvalidCredentialsError,
    MalformedTokenError, 
    InvalidTokenPayload,
    UserInactiveError,
)

from schemas.users import UserInDB

from utils.security import (
    check_password, 
    decode_jwt,
)

from db.user_repository import UsersRepo

from services.jwt_tokens import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE
)

from typing import Any, Callable, Coroutine 

http_bearer = HTTPBearer(auto_error=False)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/jwt_auth/login/'
)


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
) -> UserInDB:
    """
    Валидирует учетные данные пользователя для входа.
    """
    user_data_from_db = await UsersRepo.select_user_by_username(username)
    
    if not user_data_from_db:
        raise InvalidCredentialsError(detail='invalid username or password')
    
    if not check_password(
        password=password,
        hashed_password=user_data_from_db.hashed_password,
    ):
        raise InvalidCredentialsError(detail='invalid username or password')
    
    if not user_data_from_db.is_active:
        raise UserInactiveError()
    
    # Преобразуем данные из репозитория в Pydantic модель
    return UserInDB(
        id=user_data_from_db.id,
        username=user_data_from_db.username,
        email=user_data_from_db.email,
        hashed_password=user_data_from_db.hashed_password,
        is_active=user_data_from_db.is_active,
    )


def get_current_token_payload(
    token: str = Depends(oauth2_scheme)
) -> dict[str, Any]:
    """
    Декодирует JWT-токен и возвращает его полезную нагрузку.
    """
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        # TODO: Добавить логирование
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'invalid token error: {e}'
        )
    return payload


def validate_token_type(
    payload: dict[str, Any],
    token_type: str,
) -> bool:
    """
    Проверяет тип токена в полезной нагрузке.
    """
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise MalformedTokenError()


async def get_user_by_token_sub(
    payload: dict[str, Any]
) -> UserInDB:
    """
    Извлекает пользователя из базы данных по 'sub' (username) из полезной нагрузки токена.
    """
    username: str | None = payload.get('sub')
    if username:
        user_data_from_db = await UsersRepo.select_user_by_username(username)
        if not user_data_from_db:
            raise InvalidCredentialsError(detail='invalid username or password') 
        return UserInDB(
            id=user_data_from_db.id,
            username=user_data_from_db.username,
            email=user_data_from_db.email,
            hashed_password=user_data_from_db.hashed_password,
            is_active=user_data_from_db.is_active,
        )
    raise InvalidTokenPayload()


# Фабричная функция для создания зависимостей, проверяющих тип токена
# Возвращаемый тип фабрики: Callable, который возвращает Coroutine, который, в свою очередь, возвращает UserInDB
def get_auth_user_from_token_of_type(token_type: str) -> Callable[[dict[str, Any]], Coroutine[Any, Any, UserInDB]]:
    """
    Фабрика зависимостей, которая возвращает асинхронную функцию для получения
    аутентифицированного пользователя определенного типа токена.
    """
    async def get_auth_user_from_token(
        payload: dict[str, Any] = Depends(get_current_token_payload) # Уточнен тип payload
    ) -> UserInDB: # <-- Внутренняя функция возвращает UserInDB после выполнения
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload)
    return get_auth_user_from_token


# Создаем конкретные зависимости, используя фабрику
get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)

get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)


async def get_current_active_auth_user(
    user: UserInDB = Depends(get_current_auth_user)
) -> UserInDB:
    """
    Возвращает текущего активного аутентифицированного пользователя.
    """
    if user.is_active:
        return user
    raise UserInactiveError()

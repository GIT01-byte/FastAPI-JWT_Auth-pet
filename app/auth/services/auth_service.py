from fastapi import Response
from fastapi.responses import JSONResponse 

from schemas.users import UserInDB

from config import settings

from services.jwt_tokens import (
    REFRESH_TOKEN_TYPE,
    ACCESS_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    )

from exceptions.exceptions import (
    UserNotFoundError,
    InvalidPasswordError,
    UserInactiveError,
    )

from utils.security import check_password
from db.user_repository import UsersRepo


async def authenticate_user(
    username: str,
    password: str,
) -> Response:
    user_data_from_db = await UsersRepo.select_user_by_username(username)

    # Проверяем полученного user'а
    if not user_data_from_db:
        raise UserNotFoundError()
    
    if not check_password(
        password=password,
        hashed_password=user_data_from_db.hashed_password
        ):
        raise InvalidPasswordError()
    
    if not user_data_from_db.is_active:
        raise UserInactiveError()

    # Преобразуем данные из репозитория в Pydantic модель
    user = UserInDB(
        id=user_data_from_db.id,
        username=user_data_from_db.username,
        email=user_data_from_db.email,
        hashed_password=user_data_from_db.hashed_password,
        is_active=user_data_from_db.is_active,
    )

    # Генерируем токены
    user_id = str(user_data_from_db.id) # Обязательно делаем строчкой, для избежания ошибки "InvalidSubjectError: Subject must be a string"
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)

    # Создаем Response и устанавливаем куки
    response = Response(
        content=user.model_dump_json(), # Тело ответа - данные пользователя (без пароля)
        status_code=200,
        media_type="application/json",
    )

    # Устанавливаем куки, включая настройки безопасности
    response.set_cookie(
        key=ACCESS_TOKEN_TYPE,
        value=access_token,
        httponly=True,          # Доступно только через HTTP
        secure=True,            # Только по HTTPS (важно для продакшена)
        samesite="lax",         # Защита от CSRF
        max_age=60 * settings.jwt_auth.access_token_expire_minutes # Время жизни куки
    )
    response.set_cookie(
        key=REFRESH_TOKEN_TYPE,
        value=refresh_token,
        httponly=True,
        secure=True,            # Только по HTTPS
        samesite="lax",         # Защита от CSRF
        max_age=60 * 60 * 24 * settings.jwt_auth.refresh_token_expire_days # Время жизни куки
    )
    
    return response # Возвращаем готовый Response


def logout_user(response: JSONResponse) -> JSONResponse:
    # Удаляем куки токенов
    response.delete_cookie(ACCESS_TOKEN_TYPE)
    response.delete_cookie(REFRESH_TOKEN_TYPE)
    
    # Возвращаем статус и дополнительное сообщение для отладки
    return JSONResponse(content={"message": "Logout successful"}, status_code=200)

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from services.jwt_tokens import create_access_token

from exceptions.exceptions import (
    InvalidCredentialsError,
    PasswordRequiredError,
    )

from schemas.users import (
    LoginRequest,
    TokenResponse,
    UserInDB,
    )

from services.auth_service import authenticate_user, logout_user

from deps.auth_deps import (
    get_tokens_by_cookie,
    http_bearer,
    get_current_auth_user_for_refresh,
    get_current_token_payload,
    get_current_active_auth_user,
)


router = APIRouter(
    dependencies=[Depends(http_bearer)],
    )


@router.post('/login')
async def login_user(
    request: LoginRequest,
):
    if not request.password:
        raise PasswordRequiredError()
    user = await authenticate_user(request.username, request.password)
    if not user:
        raise InvalidCredentialsError()
    return user


# @router.post('/register')
# async def register_user(
#     request: RegisterRequest,
# ) -> TokenResponse:
#     # Подготавливаем payload без пароля (он хешируется внутри)
#     payload = {
#         'user': request.username,
#         'email': request.email,
#         'profile': request.profile,
#     }
#     user = await authenticate_user(request.username, request.password)
#     if not user:
#         raise InvalidCredentialsError()
#     return TokenResponse(
#         access_token=user["access_token"],
#         refresh_token=user["refresh_token"]
#     )


# @router.post(
#     '/refresh/',
#     response_model=TokenResponse,
#     response_model_exclude_none=True,
#     )
# async def auth_refresh_jwt(
#     user: UserInDB = Depends(get_current_auth_user_for_refresh)
# ):
#     access_token = create_access_token(user.id)
#     return TokenResponse(
#         access_token=access_token,
#     )


@router.get('/me/')
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserInDB = Depends(get_current_active_auth_user),
):
    iat = payload.get('iat')
    return {
        'username': user.username,
        'email': user.email,
        'logged_in_at': iat,
    }


@router.post("/logout/")
async def logout(
    response: JSONResponse,
    ):
    result = logout_user(response)
    return result


@router.get("/get-current-cookie/")
async def get_cookie(
    result: dict = Depends(get_tokens_by_cookie)
):
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Результат функции: get_tokens_by_cookie не найден'
    )

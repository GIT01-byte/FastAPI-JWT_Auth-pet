from fastapi import APIRouter, Depends, HTTPException, status

from exceptions.exceptions import (
    InvalidCredentialsError,
    PasswordRequiredError,
    UserAlreadyLoggedgError,
    )
from schemas.users import (
    LoginRequest,
    UserInDB,
    )
from services.auth_service import authenticate_user, logout_user, refresh_user_tokens
from deps.auth_deps import (
    get_tokens_by_cookie,
    http_bearer,
    get_current_access_token_payload,
    get_current_active_auth_user,
)


router = APIRouter(
    dependencies=[Depends(http_bearer)],
    )


@router.post('/login')
async def login_user(
    request: LoginRequest,
):
    # current_user = await get_current_active_auth_user()
    # if current_user:
    #     raise UserAlreadyLoggedgError()
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


@router.post('/refresh/')
async def auth_refresh_jwt(
    tokens: dict = Depends(get_tokens_by_cookie),
):
    refresh_token = tokens['refresh_token']
    user = refresh_user_tokens(refresh_token)
    if not user:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='Result of function: refresh_user_tokens is not realize'
        )
    return user


@router.get('/me/')
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_access_token_payload),
    user: UserInDB = Depends(get_current_active_auth_user),
):
    iat = payload.get('iat')
    return {
        'username': user.username,
        'email': user.email,
        'logged_in_at': iat,
    }


@router.post("/logout/")
async def logout():
    # TODO add exp handle (retry logging out)
    result = logout_user()
    return result


@router.get("/get-current-cookie/")
async def get_cookie(
    result: dict = Depends(get_tokens_by_cookie)
):
    return result


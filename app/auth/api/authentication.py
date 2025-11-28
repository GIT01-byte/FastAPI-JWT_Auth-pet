from fastapi import APIRouter

from exceptions.exceptions import (
    InvalidCredentialsError,
    PasswordRequiredError,
    )

from schemas.users import (
    LoginRequest, 
    RegisterRequest, 
    TokenResponse,
    )

from services.auth_service import authenticate_user


router = APIRouter()


@router.post('/login')
async def login_user(
    request: LoginRequest,
) -> TokenResponse:
    if not request.password:
        raise PasswordRequiredError()
    user = await authenticate_user(request.username, request.password)
    if not user:
        raise InvalidCredentialsError()
    return TokenResponse(
        access_token=user["access_token"],
        refresh_token=user["refresh_token"]
    )


# @router.post('/register')
# async def register_user(
#     request: RegisterRequest,
# ) -> TokenResponse:
#     payload = {

#     }
#     user = ...
#     return TokenResponse(
#         access_token=...,
#         refresh_token=...,
#     )

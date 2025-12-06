from fastapi import status
from .base import BaseAPIException

class CookieMissingTokenError(BaseAPIException):
    def __init__(self, detail: str = "Missing required cookies."):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

class InvalidCredentialsError(BaseAPIException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

class InvalidTokenPayload(BaseAPIException):
    def __init__(self, detail: str = "Invalid token payload"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

class PasswordRequiredError(BaseAPIException):
    def __init__(self, detail: str = "Password is required"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

class InvalidPasswordError(BaseAPIException):
    def __init__(self, detail: str = "Password is invalid"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

class TokenExpiredError(BaseAPIException):
    def __init__(self, detail: str = "Token has expired"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

class TokenRevokedError(BaseAPIException):
    def __init__(self, detail: str = "Token has been revoked"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

class MalformedTokenError(BaseAPIException):
    def __init__(self, detail: str = "Invalid or malformed token"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

class UserInactiveError(BaseAPIException):
    def __init__(self, detail: str = "User is not active"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)

class UserNotFoundError(BaseAPIException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)

class UserAlreadyExistsError(BaseAPIException):
    def __init__(self, detail: str = "User with this identifier already exists"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)

class RegistrationFailedError(BaseAPIException):
    def __init__(self, detail: str = "Registration failed due to internal error"):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

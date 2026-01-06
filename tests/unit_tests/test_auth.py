import fastapi
import pytest
from httpx import AsyncClient, ASGITransport
from contextlib import nullcontext as does_not_raise

from backend.auth.utils.security import create_refresh_token, hash_token
from backend.auth.core.schemas import JWTPayload
from backend.auth.main import app


class TestTokens:
    def test_create_refresh_token(self):
        token, hashed_token = create_refresh_token()
        assert isinstance(token, str)
        assert isinstance(hashed_token, str)

class TestApi:
    # TODO: ОТЛАДИТЬ ТЕСТ:
    # FAILED tests/unit_tests/test_auth.py::TestApi::test_unauthorize_user[/users/login/-POST-401] - assert 422 == 401
    # FAILED tests/unit_tests/test_auth.py::TestApi::test_unauthorize_user[/users/logout-POST-401] - assert 307 == 401
    # FAILED tests/unit_tests/test_auth.py::TestApi::test_unauthorize_user[/users/me-GET-401] - assert 307 == 401
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "url, method, st_code",
        [
            ["/users/login/", "POST", 401],
            # ["/users/tokens/refresh/", 401],
            ["/users/logout", "POST", 401],
            ["/users/me", "GET", 401],
        ]
    )
    async def test_unauthorize_user(self, url, method, st_code):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://127.0.0.1:8080"
        ) as ac:
            if method == "GET":
                response = await ac.get(url=url)
                assert response.status_code == st_code
            elif method == "POST":
                response = await ac.post(url=url)
                assert response.status_code == st_code
    
import pytest
from httpx import ASGITransport, AsyncClient

from backend.auth.main import app
from backend.auth.core.db.repositories import UsersRepo
from backend.auth.utils.security import hash_password

# TODO добавить фикстутру для хэша пароля, генерации токенов и добаления юзера в БД
# Фикстура асинхронного клиента
@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8080/users") as client:
        yield client


# Фикстура данных для тестового юзера
@pytest.fixture(scope="session")
async def user_register_payloads():
    user_register_payloads = [
    {
    "username": "test_user",
    "email": "test_user@testemail.com",
    "profile": {},
    "password": "1234test"
    },
    {
    "username": "test_user_1",
    "email": "test_user_1@testemail.com",
    "password": "5678test"
    }
    ]
    return user_register_payloads


# Фикстура для добавления тестовых юзеров в БД
@pytest.fixture(scope="session", autouse=True)
async def add_test_users(user_register_payloads):
    for user_payload in user_register_payloads:
        hashed_password = hash_password(user_payload["password"])
        db_data = user_payload.copy()
        db_data.pop("password")
        db_data["hashed_password"] = hashed_password
        await UsersRepo.create_user(db_data)


# Фикстура генерации jwt токенов для тестового юзера
# @pytest.fixture
# async def user_token():
#     pass    
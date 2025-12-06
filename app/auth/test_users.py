import asyncio
from typing import Optional
from logging import basicConfig, info, error, INFO
from secrets import token_hex

from schemas.users import UserInsertDB
from utils.security import hash_password
from db.user_repository import UsersRepo


basicConfig(level=INFO, format='%(asctime)s %(levelname)-8s %(message)s')

async def add_test_user(username: str, password: str, email: Optional[str] = None):
    """
    Добавляет тестового пользователя напрямую в базу данных.
    """
    info(f"Попытка добавить пользователя: {username}...")

    # Генерируем надежный пароль, если передан пустой
    if len(password.strip()) == 0:
        password = token_hex(16)

    # 1. Хешируем пароль
    hashed_pass = hash_password(password)

    # 2. Создаем экземпляр UserInsertDB
    new_user_data = UserInsertDB(
        username=username,
        email=email,
        hashed_password=hashed_pass,
    )

    # 3. Подключаемся к базе данных (если нужно)
    try:
        await UsersRepo.create_tables()
        info("Подключение к базе данных успешно.")

        # 4. Вставляем пользователя через репозиторий
        created_user = await UsersRepo.insert_user(new_user_data)

        info(f"✅ Пользователь '{created_user.username}' успешно добавлен.")
        info(f"ID: {created_user.id}, Username: {created_user.username}, Email: {created_user.email}, Активен: {created_user.is_active}")

    except Exception as e:
        error(f"❌ Ошибка при добавлении пользователя {username}: {e}")
    finally:
        info("Выключение...")

if __name__ == "__main__":
    # Пример использования:
    asyncio.run(add_test_user(
        username="string",
        password="string",
        email="test@example.com",
    ))

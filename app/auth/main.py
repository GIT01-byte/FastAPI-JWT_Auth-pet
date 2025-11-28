from contextlib import asynccontextmanager
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from db.user_repository import UsersRepo

from api.api import api_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await AsyncOrm.create_tables() 
    print('INFO:     База перезапущена')
    yield
    print('INFO:     Выключение...')


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
)

app.include_router(api_routers)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(f'{__name__}:app', reload=True)

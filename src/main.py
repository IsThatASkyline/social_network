from fastapi import FastAPI
from src.auth.base_config import auth_backend
from src.auth.schemas import UserRead, UserCreate
from src.social.router import router as router_blog
from src.auth.base_config import fastapi_users

app = FastAPI()

app.include_router(router_blog)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

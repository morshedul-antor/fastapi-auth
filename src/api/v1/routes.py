from fastapi import APIRouter

from .endpoints import todo, users

api_router = APIRouter()

# fmt: off
api_router.include_router(todo.router, prefix='/todo', tags=['Todos'])
api_router.include_router(users.router, prefix="/users", tags=['Users'])
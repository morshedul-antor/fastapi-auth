from schemas import TodoIn, TodoUpdate
from repositories import BaseRepo
from models import ToDo

todos_repo = BaseRepo[ToDo, TodoIn, TodoUpdate](ToDo)

from schemas import TodoIn, TodoUpdate
from repositories import BaseRepo
from models import ToDo

todo_repo = BaseRepo[ToDo, TodoIn, TodoUpdate](ToDo)

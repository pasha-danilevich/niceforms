"""Базовый пример использования."""
from nicegui import ui
from pydantic import BaseModel
from niceforms import TheBaseModelForm 
 
class User(BaseModel):
    """Some description"""
    name: str 
    age: int 
    email: str 
 
def submit_handler(user: User): 
    print(f"Пользователь создан: {user}") 
 

@ui.page('/')
def index() -> None:

    with ui.element(tag='body').classes('bg-[#009d9d] min-h-screen p-[0px] p-[30px]'):
        form = TheBaseModelForm(User, submit_callback=submit_handler)
        form.render()

ui.run()
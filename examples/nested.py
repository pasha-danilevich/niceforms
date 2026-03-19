"""Базовый пример использования."""
from nicegui import ui, APIRouter
from pydantic import BaseModel
from niceforms import BaseModelForm

router = APIRouter()

class Address(BaseModel):
    street: str
    city: str


class User(BaseModel):
    """Some description"""
    name: str
    age: int
    address: Address



@router.page('/nested')
async def nested() -> None:
    ui.query('body').style(
        'background: linear-gradient(160deg, #eff6ff 0%, #93aeff 100%);'
        'min-height: 100vh;'
    )
    ui.link(text='Назад', target='/')
    def submit_handler(user):
        print(f"Пользователь создан: {user}")


    form = BaseModelForm(User, on_submit=submit_handler)
    form.render()



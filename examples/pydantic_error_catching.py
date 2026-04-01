from nicegui import APIRouter, ui
from pydantic import BaseModel, Field

from _layout import base
from niceforms import BaseModelForm

router = APIRouter()


class User(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Z]+$",
        title="Имя",
    )

    age: int = Field(ge=14, lt=150, description="Возраст пользователя")

    salary: float = Field(ge=0, multiple_of=0.01)

    tags: list[str] = Field(min_length=1, max_length=3)


@router.page('/pydantic_error_catching')
@base
async def pydantic_error_catching() -> None:
    with ui.column().classes('w-full max-w-2xl mx-auto'):
        ui.link(text='Назад', target='/')

        async def submit_handler(user: BaseModel) -> None:
            print(f"Пользователь создан: {user}")

        form = BaseModelForm(User, on_submit=submit_handler, view_annotation_type=False)
        form.render()

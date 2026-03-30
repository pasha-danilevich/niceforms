from typing import Callable, Optional, TypeVar

from nicegui import ui
from nicegui.elements.dialog import Dialog

from .action import *
from ...ui.ui_component import UIComponent

T = TypeVar('T', bound=BaseModel)


class AddDialog(UIComponent):
    def __init__(
        self,
        on_save: SaveAction,
        form,
    ) -> None:
        self.on_save = on_save
        from niceforms import BaseModelForm

        self.form: BaseModelForm = form

    def render(self) -> Dialog:
        with ui.dialog() as dialog:
            with ui.card().classes('w-full'):
                self.form.title = 'Создать запись'
                self.form.render(as_card=False, body_classes='w-full')

                with ui.row().classes('w-full justify-end gap-2 mt-4'):
                    ui.button('Отмена', on_click=dialog.close).props('flat')
                    ui.button(
                        'Сохранить',
                        on_click=lambda: self.on_save(model=self.form.build_model()),
                    ).props('color=primary')

        return dialog


class EditDialog(UIComponent):

    def __init__(
        self,
        on_edit: EditAction,
        record_title_getter: Callable[[T], Optional[str]],
        model: BaseModel,
        index: int,
        form,
    ) -> None:
        self.on_edit = on_edit
        self.record_title_getter = record_title_getter
        self.model = model
        self.index = index
        from niceforms import BaseModelForm

        self.form: BaseModelForm = form

    def render(self) -> Dialog:
        with ui.dialog() as dialog:
            with ui.card().classes('w-full'):
                ui.label("Редактировать").classes('text-xl font-bold mb-4')

                self.form.title = self.record_title_getter(self.model)
                self.form.render(as_card=False, body_classes='w-full')
                self.form.fill(data=self.model.model_dump())

                with ui.row().classes('justify-end gap-2 mt-4'):
                    ui.button('Отмена', on_click=dialog.close).props('flat')
                    ui.button(
                        'Сохранить',
                        on_click=lambda: self.on_edit(
                            model=self.form.build_model(), index=self.index
                        ),
                    ).props('color=primary')

        return dialog


class ConfirmDeleteDialog(UIComponent):
    def __init__(self, on_confirm, record_title: str) -> None:
        self.on_confirm = on_confirm
        self.record_title = record_title

    def render(self) -> Dialog:
        with ui.dialog() as dialog:
            with ui.card():
                ui.label('Подтверждение удаления').classes('text-xl font-bold mb-4')
                ui.label(
                    f'Вы уверены, что хотите запись "{self.record_title}"?'
                ).classes('mb-4')
                with ui.row().classes('justify-end gap-2'):
                    ui.button('Отмена', on_click=dialog.close).props('flat')
                    ui.button('Удалить', on_click=self.on_confirm).props(
                        'color=negative'
                    )

        return dialog


class ViewDialog(UIComponent):

    def __init__(
        self,
        model: BaseModel,
        record_title_getter: Callable[[T], Optional[str]],
        form,
    ) -> None:
        self.model = model
        self.record_title_getter = record_title_getter
        from niceforms import BaseModelForm

        self.form: BaseModelForm = form

    def render(self) -> Dialog:
        with ui.dialog() as dialog:
            with ui.card().classes('w-full'):

                self.form.title = self.record_title_getter(self.model)
                self.form.render(as_card=False, body_classes='w-full')
                self.form.fill(data=self.model.model_dump())

                with ui.row().classes('w-full justify-end gap-2 mt-4'):
                    ui.button('Закрыть', on_click=dialog.close).props('flat')

        return dialog

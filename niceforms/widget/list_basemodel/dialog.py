from typing import Callable, Optional

from nicegui import ui
from nicegui.elements.dialog import Dialog

from .action import *
from ...ui.button import PositiveButton, DefaultButton, NegativeButton
from ...ui.ui_component import UIComponent
from ...utils import T


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
        self.form.title = 'Создать запись'
        self.form.buttons['submit'] = PositiveButton(
            text='Добавить запись',
            on_click=lambda: self.on_save(model=self.form.build_model()),
        )
        dialog = self.form.render(wrap='dialog')

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
        self.form.title = self.record_title_getter(self.model)
        self.form.buttons['submit'] = PositiveButton(
            text='Обновить запись',
            on_click=lambda: self.on_edit(
                model=self.form.build_model(), index=self.index
            ),
        )
        dialog = self.form.render(wrap='dialog')
        self.form.fill(data=self.model.model_dump())
        return dialog


class ConfirmDeleteDialog(UIComponent):
    def __init__(self, on_confirm, record_title: str, wrapper_classes: str) -> None:
        self.on_confirm = on_confirm
        self.record_title = record_title
        self.wrapper_classes = wrapper_classes
        self.wrapper_classes += ' max-w-lg'

    def render(self) -> Dialog:
        with ui.dialog() as dialog:
            with ui.card().classes(self.wrapper_classes) as self.body_element:
                ui.label('Подтверждение удаления').classes('text-xl font-bold mb-4')
                ui.label(
                    f'Вы уверены, что хотите запись "{self.record_title}"?'
                ).classes('mb-4')
                with ui.row().classes('justify-end gap-2 w-full mt-10'):
                    DefaultButton('Отмена', on_click=dialog.close).render()
                    NegativeButton('Удалить', on_click=self.on_confirm).render()

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
        self.form.title = self.record_title_getter(self.model)
        send_btn = self.form.buttons.get("submit")

        if send_btn:
            del self.form.buttons["submit"]

        dialog = self.form.render(wrap='dialog')
        self.form.fill(data=self.model.model_dump())

        for w in self.form.widgets.values():
            w.set_enabled(False)

        return dialog
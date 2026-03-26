from nicegui import ui
from nicegui.elements.dialog import Dialog

from niceforms import UIComponent
from .action import *


class AddDialog(UIComponent):
    def __init__(self, on_save: SaveAction, model_type: type[BaseModel]) -> None:
        self.on_save = on_save
        self.model_type = model_type

    def render(self) -> Dialog:
        with ui.dialog() as dialog:
            with ui.card().classes('w-full'):
                from niceforms import BaseModelForm

                form = BaseModelForm(
                    model=self.model_type,
                    view_annotation_type=False,
                    view_clear_button=False,
                    view_json_button=False,
                    view_submit_button=False,
                )
                form.render(as_card=False, body_classes='w-full')

                with ui.row().classes('w-full justify-end gap-2 mt-4'):
                    ui.button('Отмена', on_click=dialog.close).props('flat')
                    ui.button(
                        'Сохранить',
                        on_click=lambda: self.on_save(model=form.build_model()),
                    ).props('color=primary')

        return dialog


class EditDialog(UIComponent):
    def __init__(self, on_edit: EditAction, model: BaseModel) -> None:
        self.on_edit = on_edit
        self.model = model

    def render(self) -> Dialog:
        with ui.dialog() as dialog:
            with ui.card().classes('w-96'):
                ui.label("Редактировать").classes('text-xl font-bold mb-4')

                with ui.row().classes('justify-end gap-2 mt-4'):
                    ui.button('Отмена', on_click=dialog.close).props('flat')
                    ui.button(
                        # 'Сохранить', on_click=lambda: self.on_edit(name_input.value)
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

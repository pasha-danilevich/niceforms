from typing import Optional, Protocol, Callable, TypeVar, Generic

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.dialog import Dialog
from .action import *

from niceforms import UIComponent
from .dialog import AddDialog, ConfirmDeleteDialog, EditDialog, ViewDialog

T = TypeVar('T', bound=BaseModel)


class VoidRecordLine(UIComponent):
    def render(self) -> None:
        with ui.row().classes(
            'w-full justify-between items-center p-2 rounded border-2 border-dashed border-gray-300 bg-gray-50/50'
        ):
            # Скелетон для текста
            ui.element('div').classes('h-6 min-w-30 max-w-48 bg-gray-200 rounded')

            # Скелетоны для кнопок
            with ui.row().classes('gap-2'):
                for _ in range(3):  # Три скелетона для трех кнопок
                    ui.element('div').classes('h-[36px] w-[56px] bg-gray-200 rounded')


class RecordLine(UIComponent):
    def __init__(
        self,
        number: int,
        list_index: int,
        title: str,
        model: BaseModel,
        on_view: SaveAction,
        on_edit: EditAction,
        on_delete: DeleteAction,
    ) -> None:
        self.number = number
        self.list_index = list_index
        self.title = title
        self.model = model

        # actions
        self.on_view = on_view
        self.on_edit = on_edit
        self.on_delete = on_delete

    def render(self) -> None:
        with ui.row().classes(
            'w-full justify-between items-center p-2 bg-gray-50 rounded'
        ):
            ui.label(f"{self.number}. {self.title}").classes('text-lg')

            with ui.row().classes('gap-1'):
                # Кнопка "Показать" с иконкой visibility
                ui.button(
                    icon='visibility',
                    on_click=lambda: self.on_view(self.model),
                ).props('flat').classes('hover:bg-blue-50').tooltip('Показать')

                # Кнопка "Редактировать" с иконкой edit
                ui.button(
                    icon='edit',
                    on_click=lambda: self.on_edit(
                        model=self.model, index=self.list_index
                    ),
                ).props('flat').classes('hover:bg-orange-50').tooltip('Редактировать')

                # Кнопка "Удалить" с иконкой delete
                ui.button(
                    icon='delete',
                    on_click=lambda: self.on_delete(
                        model=self.model, index=self.list_index
                    ),
                ).props('flat color=negative').classes('hover:bg-red-50').tooltip(
                    'Удалить'
                )


class ListComponent(UIComponent, Generic[T]):
    def __init__(
        self,
        storage: list[T],
        record_title_getter: Callable[[T], Optional[str]],
        model: type[BaseModel],
    ) -> None:
        self.storage: list[T] = storage
        self.record_title_getter = record_title_getter
        self.model_type = model

        self.container: Optional[Element] = None

        self.dialog: Optional[Dialog] = None
        self.current_user = None
        self.is_edit_mode: bool = False

    def ensure_title(self, model: BaseModel, number: int) -> str:
        text = self.record_title_getter(model)
        return text if text is not None else f'Запись №{number}'

    def render(self) -> Element:
        """Создание интерфейса"""
        with ui.column().classes('w-full max-w-2xl mx-auto') as column:
            # Контейнер для списка пользователей
            self.container = ui.column().classes('w-full gap-2')
            self.refresh_list()

            # Кнопка добавления
            ui.button('Добавить', on_click=self.show_add_dialog)
        return column

    def refresh_list(self):
        """Обновление отображения списка пользователей"""
        self.container.clear()

        with self.container:
            for i, record in enumerate(self.storage):
                RecordLine(
                    number=i + 1,
                    list_index=i,
                    title=self.ensure_title(record, i + 1),
                    model=record,
                    on_view=self.show_info,
                    on_edit=self.show_edit_dialog,
                    on_delete=self.delete,
                ).render()

            if not self.storage:
                VoidRecordLine().render()

    def show_info(self, model: BaseModel):
        """Показать информацию о записи"""
        self.dialog = ViewDialog(model=model, model_type=self.model_type).render()
        self.dialog.open()

    def show_add_dialog(self):
        """Показать диалог добавления пользователя"""
        self.dialog = AddDialog(on_save=self.save, model_type=self.model_type).render()
        self.dialog.open()

    def show_edit_dialog(self, model: BaseModel, index: int):
        """Показать диалог редактирования пользователя"""
        self.dialog = EditDialog(
            on_edit=self.edit,
            model=model,
            index=index,
            model_type=self.model_type,
        ).render()
        self.dialog.open()

    def edit(self, model: BaseModel, index: int) -> None:
        self.storage[index] = model
        self.dialog.close()
        self.refresh_list()

    def save(self, model: BaseModel) -> None:
        """Сохранить"""
        self.storage.append(model)
        self.dialog.close()
        self.refresh_list()

    def delete(self, model: BaseModel, index: int) -> None:
        """Удалить пользователя с подтверждением"""

        def confirm_delete():
            self.storage.pop(index)
            self.refresh_list()
            dialog.close()

        dialog = ConfirmDeleteDialog(
            on_confirm=confirm_delete,
            record_title=self.ensure_title(model, index + 1),
        ).render()

        dialog.open()

from typing import Optional, Callable, Generic

from nicegui import ui, Event
from nicegui.element import Element
from nicegui.elements.button import Button

from .action import *
from .dialog import ConfirmDeleteDialog

from ...ui.button import PositiveButton

from ...ui.ui_component import UIComponent
from ...utils import T


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
        record_title_getter: Callable[[T], Optional[str]],
        number: int,
        list_index: int,
        title: str,
        model: BaseModel,
        on_edit: EditAction,
        on_delete: DeleteAction,
        kwarg: dict,
    ) -> None:
        from niceforms import BaseModelForm

        self.number = number
        self.list_index = list_index
        self.title = title
        self.model = model

        # actions
        self.on_edit = on_edit
        self.on_delete = on_delete

        # buttons
        self._view_btn: Optional[Button] = None
        self._edit_btn: Optional[Button] = None
        self._delete_btn: Optional[Button] = None

        self.read_form = BaseModelForm(type(model), **kwarg)
        self.edit_form = BaseModelForm(type(model), **kwarg)

        self.read_form.buttons = {}
        self.edit_form.buttons = {}

        # configure ReadForm
        self.read_form.title = record_title_getter(model)

        # configure EditFrom
        self.edit_form.title = record_title_getter(model)
        self.edit_form.buttons['submit'] = lambda : PositiveButton(
            text='Обновить запись',
            on_click=lambda: self.on_edit(
                model=self.edit_form.build_model(),
                index=list_index,
                dialog=self._edit_dialog,
            ),
        )

        # dialogs
        self._view_dialog = self.read_form.render(wrap='dialog')
        self._edit_dialog = self.edit_form.render(wrap='dialog')

        self.read_form.fill(data=model.model_dump())
        self.edit_form.fill(data=model.model_dump())

    @property
    def view_button(self) -> Button:
        if self._view_btn is None:
            raise ValueError("view btn is not rendered yet!")
        return self._view_btn

    @property
    def edit_button(self) -> Button:
        if self._edit_btn is None:
            raise ValueError("edit btn is not rendered yet!")
        return self._edit_btn

    @property
    def delete_button(self) -> Button:
        if self._delete_btn is None:
            raise ValueError("delete btn is not rendered yet!")
        return self._delete_btn

    def render(self) -> None:
        with ui.row().classes(
            'w-full justify-between items-center p-2 bg-gray-50 rounded-xl'
        ):
            ui.label(f"{self.number}. {self.title}").classes('text-lg ml-4')

            with ui.row().classes('gap-1'):
                # Кнопка "Показать" с иконкой visibility
                self._view_btn = (
                    ui.button(
                        icon='visibility',
                        on_click=self._open_view,
                    )
                    .props('flat round size=0.75rem')
                    .classes('hover:bg-blue-50')
                    .tooltip('Показать')
                )

                # Кнопка "Редактировать" с иконкой edit
                self._edit_btn = (
                    ui.button(
                        icon='edit',
                        on_click=self._edit_dialog.open,
                    )
                    .props('flat round size=0.75rem')
                    .classes('hover:bg-orange-50')
                    .tooltip('Редактировать')
                )

                # Кнопка "Удалить" с иконкой delete
                self._delete_btn = (
                    ui.button(
                        icon='delete',
                        on_click=lambda: self.on_delete(
                            model=self.model, index=self.list_index
                        ),
                    )
                    .props('flat round color=negative size=0.75rem')
                    .classes('hover:bg-red-50')
                    .tooltip('Удалить')
                )

    def _open_view(self) -> None:
        self.read_form.set_readonly(True)
        self._view_dialog.open()


class Column(UIComponent, Generic[T]):

    def __init__(
        self,
        model_type: type[BaseModel],
        storage: list[T],
        record_title_getter: Callable[[T], Optional[str]],
        kwarg,
    ) -> None:
        self.storage: list[T] = storage
        self.record_title_getter = record_title_getter
        self.kwarg = kwarg
        self.container: Optional[Element] = None

        self._add_button: Optional[Button] = None

        from niceforms import BaseModelForm

        self.create_form = BaseModelForm(model_type, **kwarg)

        # configure CreateForm
        self.create_form.title = 'Создать запись'
        self.create_form.buttons = {
            'submit': lambda : PositiveButton(
                text='Добавить запись',
                on_click=lambda: self.save(self.create_form.build_model()),
            )
        }
        self._create_record_dialog = self.create_form.render(wrap='dialog')

        self.records: list[RecordLine] = []
        
        self.on_refresh = Event()

    @property
    def add_button(self) -> Button:
        if not self._add_button:
            raise ValueError('Not rendered yet')

        return self._add_button

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
            self._add_button = PositiveButton(
                "",
                on_click=self._create_record_dialog.open,
                icon='add',
                
            ).classes('w-full')
        return column

    def refresh_list(self):
        """Обновление отображения списка пользователей"""
        self.container.clear()

        with self.container:
            for i, record in enumerate(self.storage):
                line = RecordLine(
                    record_title_getter=self.record_title_getter,
                    number=i + 1,
                    list_index=i,
                    title=self.ensure_title(record, i + 1),
                    model=record,
                    on_edit=self.edit,
                    on_delete=self.delete,
                    kwarg=self.kwarg,
                )
                line.render()
                self.records.append(line)

            if not self.storage:
                VoidRecordLine().render()
        
        self.on_refresh.emit()

    def edit(self, model: BaseModel, index: int, dialog: Dialog) -> None:
        self.storage[index] = model
        dialog.close()
        self.refresh_list()

    def save(self, model: BaseModel) -> None:
        """Сохранить"""
        self.storage.append(model)

        self._create_record_dialog.close()

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
            wrapper_classes='',
        ).render()

        dialog.open()

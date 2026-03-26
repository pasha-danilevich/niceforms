from typing import Optional, Protocol, Callable, TypeVar, Generic

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.dialog import Dialog
from .action import *
from niceforms import UIComponent

T = TypeVar('T', bound=BaseModel)


class AddDialog(UIComponent):
    def __init__(self, on_save: SaveAction) -> None:
        self.on_save = on_save

    def render(self) -> Dialog:
        with ui.dialog() as dialog:
            with ui.card().classes('w-96'):
                ui.label("Добавить пользователя").classes('text-xl font-bold mb-4')

                name_input = ui.input('Имя').classes('w-full mb-4')

                with ui.row().classes('justify-end gap-2 mt-4'):
                    ui.button('Отмена', on_click=dialog.close).props('flat')
                    ui.button(
                        'Сохранить', on_click=lambda: self.on_save(name_input.value)
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


class VoidRecordLine(UIComponent):
    def render(self) -> None:
        with ui.row().classes(
            'w-full justify-between items-center p-2 rounded border-2 border-dashed border-gray-300 bg-gray-50/50'
        ):
            # Скелетон для текста
            ui.element('div').classes('h-6 w-48 bg-gray-200 rounded')

            # Скелетоны для кнопок
            with ui.row().classes('gap-2'):
                for _ in range(3):  # Три скелетона для трех кнопок
                    ui.element('div').classes('h-[36px] w-[56px] bg-gray-200 rounded')


class RecordLine(UIComponent):
    def __init__(
        self,
        number: int,
        title: Optional[str],
        model,
        on_view,
        on_edit: EditAction,
        on_delete,
    ) -> None:
        self.number = number
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
                    on_click=lambda: self.on_edit(model=self.model, index=self.number),
                ).props('flat').classes('hover:bg-orange-50').tooltip('Редактировать')

                # Кнопка "Удалить" с иконкой delete
                ui.button(
                    icon='delete', on_click=lambda: self.on_delete(self.model)
                ).props('flat color=negative').classes('hover:bg-red-50').tooltip(
                    'Удалить'
                )


class ListComponent(UIComponent, Generic[T]):
    def __init__(
        self,
        storage: list[T],
        record_title_getter: Callable[[T], str],
        model: type[BaseModel],
    ) -> None:
        self.storage: list[T] = storage
        self.record_title_getter = record_title_getter
        self.model_type = model

        self.container: Optional[Element] = None

        self.dialog: Optional[Dialog] = None
        self.current_user = None
        self.is_edit_mode: bool = False

    def render(self) -> None:
        """Создание интерфейса"""
        with ui.column().classes('w-full max-w-2xl mx-auto'):
            # Контейнер для списка пользователей
            self.container = ui.column().classes('w-full gap-2')
            self.refresh_list()

            # Кнопка добавления
            ui.button('Добавить', on_click=self.show_add_dialog)

    def refresh_list(self):
        """Обновление отображения списка пользователей"""
        self.container.clear()

        with self.container:
            for i, record in enumerate(self.storage, 1):
                RecordLine(
                    number=i,
                    title=self.record_title_getter(record),
                    model=record,
                    on_view=self.show_info,
                    on_edit=lambda x, y: Person(name='', age=0),
                    on_delete=self.delete,
                ).render()

            if not self.storage:
                VoidRecordLine().render()

    def show_info(self, user):
        """Показать информацию о записи"""
        # with ui.dialog() as dialog:
        #     with ui.card():
        #         ui.label(f"Информация о записи").classes('text-xl font-bold mb-4')
        #         ui.label(f"ID: {user['id']}").classes('mb-2')
        #         ui.label(f"Имя: {user['name']}").classes('mb-4')
        #         ui.button('Закрыть', on_click=dialog.close)
        # dialog.open()
        pass

    def show_add_dialog(self):
        """Показать диалог добавления пользователя"""
        pass
        # self.is_edit_mode = False
        # self.current_user = None
        #
        # self.dialog = AddDialog(on_save=self.save).render()
        #
        # self.dialog.open()

    def show_edit_dialog(self, user):
        """Показать диалог редактирования пользователя"""
        pass
        # self.is_edit_mode = True
        # self.current_user = user
        #
        # self.dialog = EditDialog(on_edit=self.save, model=user).render()
        #
        # self.dialog.open()

    def save(self, model: BaseModel) -> None:
        """Сохранить (добавить или обновить)"""
        pass
        # if self.is_edit_mode and self.current_user:
        #     # Редактирование существующего пользователя
        #     self.current_user['name'] = model.strip()
        # else:
        #     # Добавление нового пользователя
        #     new_user = {"id": self.next_id, "name": model.strip()}
        #     self.storage.append(new_user)
        #
        # self.dialog.close()
        # self.refresh_list()

    def delete(self, user):
        """Удалить пользователя с подтверждением"""
        pass
        # def confirm_delete():
        #     self.storage.remove(user)
        #     self.refresh_list()
        #     dialog.close()
        #
        # dialog = ConfirmDeleteDialog(
        #     on_confirm=confirm_delete,
        #     record_title=user["name"],
        # ).render()
        #
        # dialog.open()

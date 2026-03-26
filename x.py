from typing import Optional

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.dialog import Dialog
from pydantic import BaseModel

from niceforms import UIComponent


class AddDialog(UIComponent):
    def __init__(self, on_save) -> None:
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
    def __init__(self, on_save, user) -> None:
        self.on_save = on_save
        self.user = user

    def render(self) -> Dialog:
        with ui.dialog() as dialog:
            with ui.card().classes('w-96'):
                ui.label("Редактировать пользователя").classes('text-xl font-bold mb-4')

                name_input = ui.input('Имя', value=self.user['name']).classes(
                    'w-full mb-4'
                )

                with ui.row().classes('justify-end gap-2 mt-4'):
                    ui.button('Отмена', on_click=dialog.close).props('flat')
                    ui.button(
                        'Сохранить', on_click=lambda: self.on_save(name_input.value)
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


class RecordLine(UIComponent):
    def __init__(
        self,
        number: int,
        title: Optional[str],
        model,
        on_view,
        on_edit,
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
                    on_click=lambda: self.on_edit(self.model),
                ).props('flat').classes('hover:bg-orange-50').tooltip('Редактировать')

                # Кнопка "Удалить" с иконкой delete
                ui.button(icon='delete', on_click=lambda: self.on_delete(self.model)).props(
                    'flat color=negative'
                ).classes('hover:bg-red-50').tooltip('Удалить')


class ListComponent(UIComponent):
    def __init__(self):
        self.storage = [
            {"id": 1, "name": "Коля"},
            {"id": 2, "name": "Вася"},
            {"id": 3, "name": "Миша"},
        ]
        self.next_id: int = 4

        self.container: Optional[Element] = None

        self.dialog: Optional[Dialog] = None
        self.current_user = None
        self.is_edit_mode: bool = False

        self.render()

    def render(self) -> None:
        """Создание интерфейса"""
        with ui.column().classes('w-full max-w-2xl mx-auto p-4'):
            # Контейнер для списка пользователей
            self.container = ui.column().classes('w-full gap-2 mb-4')
            self.refresh_list()

            # Кнопка добавления
            ui.button('Добавить', on_click=self.show_add_dialog).classes('mt-2')

    def refresh_list(self):
        """Обновление отображения списка пользователей"""
        self.container.clear()

        with self.container:
            for i, record in enumerate(self.storage, 1):
                RecordLine(
                    number=i,
                    title=record['name'],
                    model=record,
                    on_view=self.show_info,
                    on_edit=self.show_edit_dialog,
                    on_delete=self.delete,
                ).render()

    def show_info(self, user):
        """Показать информацию о записи"""
        with ui.dialog() as dialog:
            with ui.card():
                ui.label(f"Информация о записи").classes('text-xl font-bold mb-4')
                ui.label(f"ID: {user['id']}").classes('mb-2')
                ui.label(f"Имя: {user['name']}").classes('mb-4')
                ui.button('Закрыть', on_click=dialog.close)
        dialog.open()

    def show_add_dialog(self):
        """Показать диалог добавления пользователя"""
        self.is_edit_mode = False
        self.current_user = None

        self.dialog = AddDialog(on_save=self.save).render()

        self.dialog.open()

    def show_edit_dialog(self, user):
        """Показать диалог редактирования пользователя"""
        self.is_edit_mode = True
        self.current_user = user

        self.dialog = EditDialog(on_save=self.save, user=user).render()

        self.dialog.open()

    def save(self, name):
        """Сохранить (добавить или обновить)"""

        if self.is_edit_mode and self.current_user:
            # Редактирование существующего пользователя
            self.current_user['name'] = name.strip()
        else:
            # Добавление нового пользователя
            new_user = {"id": self.next_id, "name": name.strip()}
            self.storage.append(new_user)
            self.next_id += 1

        self.dialog.close()
        self.refresh_list()

    def delete(self, user):
        """Удалить пользователя с подтверждением"""

        def confirm_delete():
            self.storage.remove(user)
            self.refresh_list()
            dialog.close()

        dialog = ConfirmDeleteDialog(
            on_confirm=confirm_delete,
            record_title=user["name"],
        ).render()

        dialog.open()


# Запуск приложения
@ui.page('/')
def index():
    ListComponent()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(show=False, reload=False)

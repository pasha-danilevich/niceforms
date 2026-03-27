from datetime import datetime, date
from typing import Any, Optional

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.mixins.value_element import ValueElement

from niceforms import BaseWidget, BaseValueWidget


class DateWidget(BaseValueWidget):
    def fill(self, data: date | str) -> None:
        assert isinstance(data, date | str), 'incorrect data type: {}'.format(
            type(data)
        )

        self.element.set_value(str(data))

    def validate(self) -> Optional[str]:
        if not self.normalized_type.is_nullable and not self.element.value:
            return "Поле не может быть пустым"

        if self.element.value:
            try:
                datetime.strptime(self.element.value, "%Y-%m-%d").date()
            except ValueError:
                return "Не верный формат даты. Ожидается YYYY-MM-DD"

        return None

    def collect(self) -> Optional[Any]:

        if self.element.value in ["", None]:
            return None

        try:
            return datetime.strptime(self.element.value, "%Y-%m-%d").date()
        except ValueError:
            return None

    def render(self) -> ValueElement:
        with ui.row().classes("w-full").style(
            "display: flex; flex-direction: row; flex-wrap: nowrap;"
        ):
            el = (
                ui.date_input(placeholder='1990-01-01', on_change=self.hide_error)
                .props("outlined dense")
                .classes("w-full")
            )

            def now():
                el.set_value(datetime.now().strftime("%Y-%m-%d"))

            ui.button('Сегодня', on_click=now)
        return el


class DateTimeWidget(BaseWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._date_input: Optional[ValueElement] = None
        self._time_input: Optional[ValueElement] = None

    def fill(self, data: datetime | str) -> None:
        assert isinstance(data, (datetime, str)), 'incorrect data type: {}'.format(
            type(data)
        )

        # Преобразуем строку в datetime если нужно
        if isinstance(data, str):
            try:
                # Пробуем парсить ISO формат или формат с пробелом
                data = datetime.fromisoformat(data.replace('Z', '+00:00'))
            except ValueError:
                try:
                    data = datetime.strptime(data, "%Y-%m-%d %H:%M")
                except ValueError:
                    # Если не удалось, оставляем как строку
                    date_str = data
                    time_str = data
                    self._date_input.set_value(date_str)
                    self._time_input.set_value(time_str)
                    return

        # Если data - datetime объект
        if isinstance(data, datetime):
            # Форматируем дату и время
            date_str = data.strftime("%Y-%m-%d")
            time_str = data.strftime("%H:%M")

            # Устанавливаем значения
            self._date_input.set_value(date_str)
            self._time_input.set_value(time_str)

    def validate(self) -> Optional[str]:
        if not self._date_input.value and not self.normalized_type.is_nullable:
            return "Поле Дата не может быть пустым"
        if not self._time_input.value and not self.normalized_type.is_nullable:
            return "Поле Время не может быть пустым"

        if self._date_input.value and self._time_input.value:
            try:
                datetime.strptime(
                    f"{self._date_input.value} {self._time_input.value}",
                    "%Y-%m-%d %H:%M",
                )
            except ValueError:
                return "Не верный формат времени. Ожидается YYYY-MM-DD HH:MM"

        return None

    def collect(self) -> Optional[datetime]:
        if self._date_input.value and self._time_input.value:
            try:
                return datetime.strptime(
                    f"{self._date_input.value} {self._time_input.value}",
                    "%Y-%m-%d %H:%M",
                )
            except ValueError:
                return None

        return None

    def clear(self) -> None:
        self._date_input.set_value(None)
        self._time_input.set_value(None)

    def render(self) -> Element:
        with ui.row().classes("w-full").style(
            "display: flex; flex-direction: row; flex-wrap: nowrap;"
        ) as row:
            self._date_input = (
                ui.date_input(placeholder='1990-01-01', on_change=self.hide_error)
                .props("outlined dense")
                .classes("w-full")
            )
            self._time_input = (
                ui.time_input(placeholder='12:00', on_change=self.hide_error)
                .props("outlined dense")
                .classes("")
            )

            def now():
                self._date_input.set_value(datetime.now().strftime("%Y-%m-%d"))
                self._time_input.set_value(datetime.now().strftime("%H:%M"))

            ui.button('Сейчас', on_click=now)

        return row

from datetime import datetime
from typing import Optional, Any

from nicegui.elements.mixins.value_element import ValueElement
from nicegui import ui
from niceforms import BaseWidget


class DateWidget(BaseWidget):
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

    def render(self) -> ValueElement:
        with ui.row().classes("w-full").style(
            "display: flex; flex-direction: row; flex-wrap: nowrap;"
        ):
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

        return ValueElement(value='')

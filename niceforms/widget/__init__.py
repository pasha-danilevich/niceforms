"""Виджеты для полей формы."""
from abc import ABC, abstractmethod
from typing import Any, Optional

from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from niceforms import UIComponent


class BaseWidget(UIComponent, ABC):
    def __init__(self, field_info: FieldInfo, field_name: str):
        self.field = field_info
        self.field_name = field_name

    @property
    def placeholder(self) -> str:
        return f'Введите {self.field.title.lower()}' if self.field.title else 'Введите значение'

    @property
    def default_value(self) -> Optional[Any]:
        return self.field.default if self.field.default is not PydanticUndefined else None

    def render_label(self) -> None:
        text = self.field.title if self.field.title else self.field_name.title()
        text = text + ' *' if self.field.is_required() else text

        ui.label(text=text).classes('mb-1 font-bold text-lg')
        if self.field.description:
            ui.label(text=self.field.description).classes('mb-1 text-gray-500')  # как сделать это поле серым

    @abstractmethod
    def render(self) -> "RenderedWidget": # TODO: возможно достаточно будет в RenderedWidget передавать в место BaseWidget "field_name"
        raise NotImplementedError


class RenderedWidget(ABC):
    def __init__(self, widget: BaseWidget, element: ValueElement) -> None:
        self.widget = widget
        self.element = element

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def collect(self) -> Any:
        raise NotImplementedError
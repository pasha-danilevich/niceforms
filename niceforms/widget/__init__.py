"""Виджеты для полей формы."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

from nicegui import ui
from nicegui.elements.button import Button
from nicegui.elements.mixins.value_element import ValueElement
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from niceforms import UIComponent
from utils import NormalizedType

logger = logging.getLogger(__name__)


class BaseWidget(UIComponent, ABC):
    def __init__(
        self,
        field_info: FieldInfo,
        field_name: str,
        normalized_type: NormalizedType,
        view_annotation_type: bool,
    ):
        self.field = field_info
        self.field_name = field_name
        self.normalized_type = normalized_type
        self.view_annotation_type = view_annotation_type

        self.clear_button: Optional[Button] = None

    @property
    def placeholder(self) -> str:
        return (
            f"Введите {self.field.title.lower()}"
            if self.field.title
            else "Введите значение"
        )

    @property
    def default_value(self) -> Optional[Any]:
        return (
            self.field.default if self.field.default is not PydanticUndefined else None
        )

    def render_label(self) -> None:
        text = self.field.title if self.field.title else self.field_name.title()
        logger.debug(f"render label: {text}")

        with ui.row().classes('mb-1 items-baseline justify-between w-full gap-1'):
            with ui.row().classes('items-baseline gap-1'):
                ui.label(text=text).classes('font-bold text-lg')
                if self.field.is_required():
                    ui.label(text='*').classes('text-gray-400 text-md font-normal')
                if self.view_annotation_type:
                    ui.label(text=f' [{self.field.annotation}]').classes(
                        'text-gray-400 text-md font-normal'
                    )

            self.clear_button = (
                ui.button(icon='close', color='secondary')
                .props('flat dense round')
                .classes('text-xs opacity-30 hover:opacity-80 transition-opacity')
                .tooltip('Очистить')
            )

        if self.field.description:
            ui.label(text=self.field.description).classes("mb-1 text-gray-500")

    @abstractmethod
    def render(
        self,
    ) -> (
        "RenderedWidget"
    ):  # TODO: возможно достаточно будет в RenderedWidget передавать в место BaseWidget "field_name"
        raise NotImplementedError


class RenderedWidget(ABC):
    def __init__(self, widget: BaseWidget, element: ValueElement) -> None:
        self.widget = widget
        self.element = element

        self.widget.clear_button.on_click(self.clear)

    def clear(self) -> None:
        self.element.set_value(None)

    @abstractmethod
    def collect(self) -> Optional[Any]:
        raise NotImplementedError

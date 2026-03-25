"""Виджеты для полей формы."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional, cast

from nicegui import ui
from nicegui.elements.mixins.validation_element import ValidationElement
from nicegui.elements.mixins.value_element import ValueElement
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
from utils import NormalizedType

from niceforms import UIComponent

logger = logging.getLogger(__name__)


class BaseWidget(UIComponent, ABC):
    LEFT_PEDDING_PX: int = 7

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

        self._rendered_element: Optional[ValueElement] = None

        self.default_validations = {}
        if not normalized_type.is_nullable:
            self.default_validations = {
                'Поле не может быть пустым': lambda v: (
                    False if v is None or v == '' else True
                )
            }

    def set_element(self, element: ValueElement) -> None:
        assert isinstance(element, ValueElement), f'Element must be a ValueElement. "{type(element)}" is no valid. Please check the correctness of the implemented "render" method in your widget "{self.__class__.__name__}"'
        self._rendered_element = element

    @property
    def element(self) -> ValueElement:
        assert self._rendered_element is not None, 'Widget has not been rendered yet.'
        return self._rendered_element

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

        with ui.row().classes('mb-1 items-baseline justify-between w-full gap-1'):
            with ui.row().classes('items-baseline gap-1').style(
                f'padding-left: {self.LEFT_PEDDING_PX}px;'
            ):
                ui.label(text=text).classes('font-medium text-base')
                if not self.normalized_type.is_nullable:
                    ui.label(text='*').classes('text-gray-400 text-md font-normal')
                if self.view_annotation_type:
                    ui.label(text=f' [{self.field.annotation}]').classes(
                        'text-gray-400 text-md font-normal'
                    )

            (
                ui.button(icon='close', color='secondary')
                .on_click(self.clear)
                .props('flat dense round')
                .classes('text-xs opacity-30 hover:opacity-80 transition-opacity')
                .tooltip('Очистить')
            )

        if self.field.description:
            ui.label(text=self.field.description).classes("mb-1 text-gray-500").style(
                f'padding-left: {self.LEFT_PEDDING_PX}px;'
            )

    def clear(self) -> None:
        self.element.set_value(None)

        if isinstance(self.element, ValidationElement):
            self.element.error = None

    @abstractmethod
    def collect(self) -> Optional[Any]:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> ValueElement:
        raise NotImplementedError

    def __repr__(self) -> str:
        """Возвращает строковое представление виджета."""
        widget_type = self.__class__.__name__
        return (
            f"{widget_type}('{self.field_name}')"
            f"[{self.normalized_type}]"
            f"{' = ' + repr(self._rendered_element.value) if self._rendered_element and self._rendered_element.value is not None else ''}"
        )

"""Виджеты для полей формы."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional, cast

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.mixins.text_element import TextElement
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
        self._error_label: Optional[TextElement] = None
        self._error_icon: Optional[Element] = None

        self.default_validations = {}
        if not normalized_type.is_nullable:
            self.default_validations = {
                'Поле не может быть пустым': lambda v: (
                    False if v is None or v == '' else True
                )
            }

    def view_error(self, error: str) -> None:
        if self._error_label:
            self._error_icon.set_visibility(True)
            self._error_label.set_visibility(True)
            self._error_label.set_text(error)

    def hide_error(self) -> None:
        if self._error_label:
            self._error_icon.set_visibility(False)
            self._error_label.set_visibility(False)

    def validate(self) -> Optional[str]:
        """Метод вызывается, когда происходит событие CollectFormData.
        Работает только у виджетов, чей элемент является ValidationElement.
        В случаях когда элемент не является ValidationElement, данный метод можно переопределить.
        """

        if self.can_element_validate():
            el = cast(ValidationElement, self.element)
            el.validate()
            return el.error

        return None

    def can_element_validate(self) -> bool:
        """Умеет ли виджет валидировать свои значения. Является ли его элемент ValidationElement."""
        if isinstance(self.element, ValidationElement):
            return True

        return False

    def set_element(self, element: ValueElement) -> None:
        assert isinstance(
            element, ValueElement
        ), f'Element must be a ValueElement. "{type(element)}" is no valid. Please check the correctness of the implemented "render" method in your widget "{self.__class__.__name__}"'
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

        if self._error_label:
            self.hide_error()

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
            f"{' = ' + repr(self._rendered_element.value) if self._rendered_element and self._rendered_element.value is not None else ' None'}"
        )

    def render_error(self) -> None:

        with ui.element().style(
            'color: #c10015; padding-left: 12px; padding-top: 8px; min-height: 20px;'
        ):
            with ui.row().classes('gap-1'):
                self._error_icon = ui.icon('error').classes('mr-1')
                self._error_label = ui.label().style('font-size: 11px;')

        self._error_label.set_visibility(False)
        self._error_icon.set_visibility(False)

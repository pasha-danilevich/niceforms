"""Виджеты для полей формы."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional, Callable, Union, Self

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.button import Button
from nicegui.elements.mixins.disableable_element import DisableableElement
from nicegui.elements.mixins.text_element import TextElement
from nicegui.elements.mixins.validation_element import ValidationElement
from nicegui.elements.mixins.value_element import ValueElement
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from ..ui.ui_component import UIComponent
from ..utils import NormalizedType, normalize_type

logger = logging.getLogger(__name__)
UnionElement = Union[Element, ValueElement, ValidationElement]


class WidgetLabel(UIComponent):
    LEFT_PEDDING_PX: int = 7
    
    def __init__(
        self,
        field_info: FieldInfo,
        field_name: str,
        normalized_type: NormalizedType,
        view_annotation_type: bool,
        on_clear: Callable[[], None],
    ) -> None:
        self.field = field_info
        self.field_name = field_name
        self.normalized_type = normalized_type
        self.view_annotation_type = view_annotation_type
        self.on_clear = on_clear
        
        self._close_button: Optional[Button] = None
    
    @property
    def close_button(self) -> Button:
        if not self._close_button:
            raise ValueError('Not rendered yet')
        return self._close_button
    
    def render(self) -> None:
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
            
            self._close_button = (
                ui.button(icon='close', color='secondary')
                .on_click(self.on_clear)
                .props('flat dense round')
                .classes('text-xs opacity-30 hover:opacity-80 transition-opacity')
                .tooltip('Очистить')
            )
        
        if self.field.description:
            ui.label(text=self.field.description).classes("mb-1 text-gray-500").style(
                f'padding-left: {self.LEFT_PEDDING_PX}px;'
            )


class BaseWidget(UIComponent, ABC):
    NO_ASSEMBLED_ERROR_MESSAGE = 'The widget is not assembled yet. Use BaseModelForm .custom_widget() instead to correct usage.'

    def __init__(
        self,
        field_info: FieldInfo,
        field_name: str,
        **kwargs: Any,
    ):
        self.props = kwargs
        self.field = field_info
        self.field_name = field_name
        self.normalized_type = normalize_type(field_info.annotation)
        self.placeholder_getter = kwargs.get('placeholder_getter', self.default_placeholder_getter)

        self.view_annotation_type = kwargs.get('view_annotation_type', False)

        self._rendered_element: Optional[Element] = None
        self._error_label: Optional[TextElement] = None
        self._error_icon: Optional[Element] = None
        self._label: Optional[WidgetLabel] = None
        self._container: Optional[Element] = None
        
        from .. import BaseModelForm
        from .list_basemodel import ListBaseModelWidget

        self._form: Optional[BaseModelForm] = None
        self._column: Optional[ListBaseModelWidget] = None

    @abstractmethod
    def fill(self, data: Optional[Any]) -> None:
        """Вызывается, когда в BaseModelForm вызывают метод .fill()"""
        raise NotImplementedError()

    @abstractmethod
    def validate(self) -> Optional[str]:
        """Метод вызывается, когда происходит событие CollectFormData.
        Работает только у виджетов, чей элемент является ValidationElement.
        В случаях когда элемент не является ValidationElement, данный метод можно переопределить.
        """
        raise NotImplementedError()
    
    @abstractmethod
    def set_enabled(self, value: bool) -> None:
        raise NotImplementedError()

    @abstractmethod
    def set_readonly(self, value: bool) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def collect(self) -> Optional[Any]:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> Element:
        raise NotImplementedError

    @property
    def form(self):
        if self._form is None:
            raise ValueError(f"Current widget {self.__class__.__name__} does not support .form within himself. Only BaseModel field support .form")
        return self._form
    
    @property
    def column(self):
        if self._column is None:
            raise ValueError(f"Current widget {self.__class__.__name__} does not support .column within himself. Only list[BaseModel] field support .column")
        return self._column
    
    @property
    def label(self) -> WidgetLabel:
        if self._label is None:
            raise ValueError('Not rendered yet')
        return self._label
    
    @property
    def element(self) -> Element:
        assert self._rendered_element is not None, 'Widget has not been rendered yet.'
        return self._rendered_element

    @property
    def container(self) -> Element:
        if not self._container:
            raise ValueError('Widget has not been rendered yet.')
        return self._container

    @property
    def placeholder(self) -> str:
        if self.placeholder_getter:
            return self.placeholder_getter(self)
        else:
            return self.default_placeholder_getter(self)

    @property
    def default_value(self) -> Optional[Any]:
        return (
            self.field.default if self.field.default is not PydanticUndefined else None
        )

    def set_container(self, container: Element) -> None:
        self._container = container

    def set_visibility(self, value: bool) -> None:
        self.container.set_visibility(value)

    def render_error(self) -> None:

        with ui.element().style(
            'color: #c10015; padding-left: 12px; padding-top: 8px; min-height: 20px;'
        ):
            with ui.row().classes('gap-1'):
                self._error_icon = ui.icon('error').classes('mr-1')
                self._error_label = ui.label().style('font-size: 11px;')

        self._error_label.set_visibility(False)
        self._error_icon.set_visibility(False)

    def render_label(self) -> None:
        self._label = WidgetLabel(
            field_info=self.field,
            field_name=self.field_name,
            normalized_type=self.normalized_type,
            view_annotation_type=self.view_annotation_type,
            on_clear=self.clear,
        )
        self.label.render()

    def view_error(self, error: str) -> None:
        if self._error_label:
            self._error_icon.set_visibility(True)
            self._error_label.set_visibility(True)
            self._error_label.set_text(error)
        # else:
        #     self.element.error = error

    def hide_error(self) -> None:
        if self._error_label:
            self._error_icon.set_visibility(False)
            self._error_label.set_visibility(False)
    
    def default_placeholder_getter(self, widget: 'BaseWidget') -> str:
        return (
            f"Введите {self.field.title.lower()}"
            if self.field.title
            else "Введите значение"
        )
    
    def _set_element(self, element: Element, expected_type: type) -> None:
        assert isinstance(
            element, expected_type
        ), f'Element must be a {expected_type}. "{type(element)}" is not valid.'
        self._rendered_element = element

    def set_element(self, element: Element) -> None:
        self._set_element(element, Element)

    def __repr__(self) -> str:
        widget_type = self.__class__.__name__
        value_repr = ''
        if self._rendered_element:
            try:
                value = getattr(self._rendered_element, 'value', None)
                value_repr = f' = {repr(value)}' if value is not None else ' None'
            except:
                value_repr = ' <value_error>'

        return f"{widget_type}('{self.field_name}')[{self.normalized_type}]{value_repr}"


class BaseValueWidget(BaseWidget, ABC):
    @abstractmethod
    def render(self) -> ValueElement:
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> Optional[str]:
        """Метод вызывается, когда происходит событие CollectFormData.
        Работает только у виджетов, чей элемент является ValidationElement.
        В случаях когда элемент не является ValidationElement, данный метод можно переопределить.
        """
        raise NotImplementedError()
    
    def set_enabled(self, value: bool) -> None:
        if not isinstance(self.element, DisableableElement):
            raise NotImplementedError('Widget does not support set_enabled(), because it does not have DisableableElement. Implement method set_enabled() in widget')
        
        el: DisableableElement = self.element  # type: ignore
        el.set_enabled(value)
        self.label.close_button.set_visibility(value)

    def set_readonly(self, value: bool) -> None:
        if value:
            self.label.close_button.set_visibility(False)
            self.element.props("readonly")
        else:
            self.label.close_button.set_visibility(True)
            self.element.props(remove="readonly")
        
    @property
    def element(self) -> ValueElement:
        return super().element  # type: ignore

    def fill(self, data: Optional[Any]) -> None:
        """Вызывается, когда в BaseModelForm вызывают метод .fill()"""
        self.element.set_value(data)

    def clear(self) -> None:
        self.element.set_value(None)

        if isinstance(self.element, ValidationElement):
            self.element.error = None

        if self._error_label:
            self.hide_error()

    def set_element(self, element: ValueElement) -> None:
        self._set_element(element, ValueElement)


class BaseValidationWidget(BaseValueWidget, ABC):

    @abstractmethod
    def render(self) -> ValidationElement:
        raise NotImplementedError

    @property
    def default_validations(self) -> dict[str, Callable]:

        def is_empty(value: Any) -> bool:
            if value is None:
                return True
            if isinstance(value, str) and value == '':
                return True
            return False

        if not self.normalized_type.is_nullable:
            return {'Поле не может быть пустым': lambda v: not is_empty(v)}
        return {}

    @property
    def element(self) -> ValidationElement:
        return super().element  # type: ignore

    def clear(self) -> None:
        self.element.set_value(None)
        self.element.error = None

    def validate(self) -> Optional[str]:
        self.element.validate()
        return self.element.error

    def set_element(self, element: ValidationElement) -> None:
        self._set_element(element, ValidationElement)

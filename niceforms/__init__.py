import logging
from typing import Any, Generic, Optional, Type, TypeVar, cast

from actions import OnSubmit
from constants import *
from exceptions import FormError
from nicegui import ui
from nicegui.elements.mixins.validation_element import ValidationElement
from pydantic import BaseModel, ConfigDict
from pydantic.fields import FieldInfo
from ui import UIComponent
from ui.body import Body
from ui.footer import Footer
from ui.header import Header
from utils import (
    NestedModel,
    get_nested_models,
    normalize_type,
    only_validation_elements,
)
from widget import BaseWidget
from widget_factory import WidgetFactory

T = TypeVar("T", bound=BaseModel)
logger = logging.getLogger(__name__)
factory = WidgetFactory()


class NestedForm(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    form: "BaseModelForm"
    model: NestedModel


class BaseModelForm(UIComponent, Generic[T]):
    def __init__(
        self,
        model: Type[BaseModel],
        on_submit: Optional[OnSubmit] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        header_bg_color: Optional[str] = None,
        view_annotation_type: bool = True,
        view_clear_button: bool = True,
        view_json_button: bool = True,
        view_submit_button: bool = True,
        _is_nullable: bool = False,
    ) -> None:
        """Initialize universal form.

        Args:
            model: Pydantic model class
            on_submit: Callback function for form submission
            title: Form title (if None, uses model name)
        """
        self.model = model
        self.on_submit = on_submit
        self.title = title or model.__name__
        self.description = description or self.model.__doc__
        self.header_bg_color = header_bg_color
        self.view_annotation_type = view_annotation_type
        self.view_clear_button = view_clear_button
        self.view_json_button = view_json_button
        self.view_submit_button = view_submit_button
        self._is_nullable = _is_nullable

        self.nested_models = get_nested_models(self.model)
        self.fields: dict[str, FieldInfo] = self.model.model_fields  # type: ignore

        # style
        self._card = None  # тело всей формы
        self._is_nested = False
        self._widgets: Optional[list[BaseWidget]] = None

        # storage
        self._nested_forms: list[NestedForm] = []
        self._header: Optional[Header] = None

    @property
    def widgets(self) -> list[BaseWidget]:
        """Все виджеты формы"""

        assert self._widgets is not None, 'Form has not been rendered yet.'
        return self._widgets

    def clear(self) -> None:
        logger.debug(f'Cleared form: {self.title}')
        for w in self.widgets:
            w.clear()

        for n in self._nested_forms:
            n.form.clear()

        validation_elements: list[ValidationElement] = only_validation_elements(
            [w.element for w in self.widgets]
        )
        for element in validation_elements:
            element.error = None

        self._header.hidde_error_icon()

    def collect_data(self, ignore_error: bool = False) -> dict[str, Any]:
        """Собирать данные введенные в виджетах

        :raise FormError если есть хотя-бы в одном виджете есть ошибка"""

        data: dict[str, Any] = {}
        errors: list[str] = []

        for w in self.widgets:
            error = w.validate()

            if error:
                w.view_error(error)
                errors.append(error)
                self._header.view_error_icon()

            logger.debug(f'Collecting data from: {w}')
            data[w.field_name] = w.collect()

        for n in self._nested_forms:
            logger.debug(
                f'Collecting form data for "{n.form.title}". is_none={n.form._header.is_none}'
            )
            data[n.model.field_name] = (
                None if n.form._header.is_none else n.form.build_model()
            )

        if errors and not ignore_error:
            ui.notify(f"Исправьте ошибки в форме: {self.title}")
            raise FormError(form_name=self.title)

        return data

    def build_model(self) -> T:
        """Собирать данные введенные в виджетах с помощью метода .collect_date()
        и создать BaseModel объект. Не игнорирует ошибки валидации в виджетах"""
        data = self.collect_data(ignore_error=False)
        return self.model(**data)

    def render(self) -> None:
        """Render the form UI."""
        logger.debug(f'Rendering form "{self.model.__name__}"')

        fields_without_nested: dict[str, FieldInfo] = {}

        for field_name, field_info in self.fields.items():
            if field_name not in [n.field_name for n in self.nested_models]:
                fields_without_nested[field_name] = field_info

        widgets = factory.build(
            model_fields=fields_without_nested,
            view_annotation_type=self.view_annotation_type,
        )

        with ui.card().classes(
            f"p-2 w-full {DEFAULT_FORM_WIDTH} shadow-lg rounded-xl overflow-hidden sm:p-4"
        ) as self._card:
            self._header = Header(
                title=self.title,
                description=self.description,
                bg_color=self.header_bg_color,
                parent_card=self._card,
                is_nested=self._is_nested,
                is_nullable=self._is_nullable,
            )
            self._header.render()

            rendered_widgets = Body(widgets).render()
            self._widgets = rendered_widgets

            for n_model in self.nested_models:
                title = n_model.field_info.title
                normalized_type = normalize_type(n_model.field_info.annotation)
                nested_form = BaseModelForm(
                    model=n_model.model,
                    title=title if title else n_model.field_name,
                    description=n_model.field_info.description,
                    header_bg_color=NESTED_FORM_BG_COLOR,
                    on_submit=None,
                    view_json_button=False,
                    view_annotation_type=self.view_annotation_type,
                    view_clear_button=False,
                    _is_nullable=normalized_type.is_nullable,
                )
                nested_form._is_nested = True
                nested_form.render()
                nested_form._card.style('height: 100px')

                self._nested_forms.append(NestedForm(form=nested_form, model=n_model))

            if not self._is_nested:
                Footer(
                    model=self.model,
                    on_submit=self.on_submit,
                    on_collect=self.build_model,
                    on_clear=self.clear,
                    view_clear_button=self.view_clear_button,
                    view_json_button=self.view_json_button,
                    view_submit_button=self.view_submit_button,
                ).render()

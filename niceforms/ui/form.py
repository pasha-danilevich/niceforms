import logging
from typing import Any, Generic, Optional, Type, TypeVar

from nicegui import ui
from pydantic import BaseModel, ConfigDict
from pydantic.fields import FieldInfo

from .ui_component import UIComponent
from ..actions import OnSubmit
from ..constants import *
from ..exceptions import FormError, FieldNotFound, CustomizationError
from ..ui.body import Body
from ..ui.footer import Footer
from ..ui.header import Header
from ..utils import (
    NestedModel,
    get_nested_models,
    normalize_type,
)
from ..widget import BaseWidget

T = TypeVar("T", bound=BaseModel)
logger = logging.getLogger(__name__)


class NestedForm(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    form: "BaseModelForm"
    model: NestedModel


class BaseModelForm(UIComponent, Generic[T]):
    DEFAULT_CLASSES = (
        f"p-2 w-full {DEFAULT_FORM_WIDTH} shadow-lg rounded-xl overflow-hidden sm:p-4"
    )

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
        from ..widget_factory import WidgetFactory

        self.factory = WidgetFactory(model)

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
        self._is_rendered: bool = False

        self.nested_models = get_nested_models(self.model)
        self.fields: dict[str, FieldInfo] = self.model.model_fields  # type: ignore # field_name: FieldInfo

        # style
        self.body_element = None  # тело всей формы
        self._is_nested = False
        self.widgets: dict[str, BaseWidget] = {}  # field_name: BaseWidget

        fields_without_nested: dict[str, FieldInfo] = {}

        for field_name, field_info in self.fields.items():
            if field_name not in [n.field_name for n in self.nested_models]:
                fields_without_nested[field_name] = field_info

        for field_name, field_type in fields_without_nested.items():
            w = self.factory.build(field_name=field_name)

            self.widgets[field_name] = w

        # storage
        self._nested_forms: list[NestedForm] = []
        self._header: Optional[Header] = None

    def custom_widget(
        self,
        field_name: str,
        widget: type[BaseWidget],
        **kwargs,
    ) -> None:
        if self._is_rendered:
            raise CustomizationError()

        if field_name not in self.fields.keys():
            raise FieldNotFound(field_name)

        self.widgets[field_name] = self.factory.build(
            widget_type=widget,
            field_name=field_name,
            kwargs=kwargs,
        )

    def fill(self, data: dict[str, Any]) -> None:
        """Наполнить виджеты данными"""

        for field_name, value in data.items():
            if w := self.widgets.get(field_name):
                w.fill(value)

        for n in self._nested_forms:
            if d := data.get(n.model.field_name):
                n.form.fill(d)

    def clear(self) -> None:
        logger.debug(f'Cleared form: {self.title}')
        for w in self.widgets.values():
            w.clear()

        for n in self._nested_forms:
            n.form.clear()

        self._header.hidde_error_icon()

    def collect_data(self, validate: bool = True) -> dict[str, Any]:
        """Собирать данные введенные в виджетах

        :raise FormError если есть хотя-бы в одном виджете есть ошибка"""

        data: dict[str, Any] = {}
        errors: list[str] = []

        for w in self.widgets.values():
            error = w.validate() if validate else None

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
                None
                if n.form._header.is_none
                else n.form.collect_data(validate=validate)
            )

        if errors:
            ui.notify(f"Исправьте ошибки в форме: {self.title}")
            raise FormError(form_name=self.title)

        return data

    def build_model(self) -> T:
        """Собирать данные введенные в виджетах с помощью метода .collect_date()
        и создать BaseModel объект. Не игнорирует ошибки валидации в виджетах"""
        data = self.collect_data()
        return self.model(**data)

    def render(
        self,
        as_card: bool = True,
        body_classes: Optional[str] = None,
    ) -> None:
        """Render the form UI."""

        body_classes: str = (
            body_classes if body_classes is not None else self.DEFAULT_CLASSES
        )

        logger.debug(f'Rendering form "{self.model.__name__} {as_card=}"')

        body_element = ui.card if as_card else ui.element

        with body_element().classes(body_classes) as self.body_element:
            self._header = Header(
                title=self.title,
                description=self.description,
                bg_color=self.header_bg_color,
                parent_card=self.body_element,
                is_nested=self._is_nested,
                is_nullable=self._is_nullable,
            )
            self._header.render()

            Body(
                widgets=list(self.widgets.values()),
                view_annotation=self.view_annotation_type,
            ).render()

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
                nested_form.body_element.style('height: 100px')

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

            self._is_rendered = True

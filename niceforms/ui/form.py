import logging
from typing import (
    Any,
    Generic,
    Optional,
    Type,
    overload,
    Literal,
)

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.card import Card
from nicegui.elements.dialog import Dialog
from pydantic import BaseModel, ConfigDict, ValidationError
from pydantic.fields import FieldInfo

from .button import FormButton
from .json_viewer import JsonDialog
from .ui_component import UIComponent
from ..actions import OnSubmit
from ..constants import *
from ..exceptions import FormError, FieldNotFound, CustomizationError
from ..i18n import tr
from ..ui.body import Body
from ..ui.footer import Footer
from ..ui.header import Header
from ..utils import NestedModel, T
from ..widget import BaseWidget

logger = logging.getLogger(__name__)


class NestedForm(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    form: "BaseModelForm"
    model: NestedModel


class BaseModelForm(UIComponent, Generic[T]):

    def __init__(
        self,
        model: Type[T],
        on_submit: Optional[OnSubmit] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        header_bg_color: Optional[str] = None,
        view_annotation_type: bool = False,
        view_type_error_message: bool = True,
        _is_nullable: bool = False,
    ) -> None:

        from ..widget_factory import WidgetFactory

        self.factory = WidgetFactory(
            model, view_annotation_type, view_type_error_message
        )

        self.model = model
        self.on_submit = on_submit
        self.title = title or model.__name__
        self.description = description or self.model.__doc__
        self.header_bg_color = header_bg_color

        self._is_nullable = _is_nullable
        self._is_rendered: bool = False

        self.fields: dict[str, FieldInfo] = self.model.model_fields  # type: ignore # field_name: FieldInfo
        self.buttons: dict[str, FormButton] = {
            "clear": FormButton(
                text="Очистить",
                on_click=self.clear,
                bg_color='gray',
                classes='px-8',
                style='color: gray',
            ),
            "json": FormButton(
                text="Показать json",
                on_click=self.render_json_viewer_dialog,
                bg_color='gray',
                classes='px-8',
                style='color: gray',
            ),
            "submit": FormButton(
                text="Отправить",
                on_click=self.submit,
                bg_color='green',
                classes='px-12',
                color_weight=500,
                style='color: white',
            ),
        }

        # style
        self.wrapper_classes = f"p-2 w-full {DEFAULT_FORM_WIDTH} shadow-lg rounded-xl overflow-hidden sm:p-4 gap-0"
        self.body_element = None  # тело всей формы
        self._is_nested = False
        self.widgets: dict[str, BaseWidget] = {}  # field_name: BaseWidget

        for field_name, field_type in self.fields.items():
            w = self.factory.build(field_name=field_name)

            self.widgets[field_name] = w

        self.header: Optional[Header] = None

    async def submit(self) -> None:
        if self.on_submit is not None:
            try:
                base_model = self.build_model()
            except FormError:
                return

            result = self.on_submit(base_model)

            import inspect

            if inspect.isawaitable(result):
                await result

        logger.warning(f"on_submit function do not provided")

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

    def fill(self, data: dict[str, Any] | None) -> None:
        """Наполнить виджеты данными"""
        if data is None:
            return

        for field_name, value in data.items():
            if w := self.widgets.get(field_name):
                w.fill(value)

    def clear(self) -> None:
        logger.debug(f'Cleared form: {self.title}')
        for w in self.widgets.values():
            w.clear()

        self.header.hidde_error_icon()

    def set_enabled(self, value: bool) -> None:
        for w in self.widgets.values():
            w.set_enabled(value)

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
                self.header.view_error_icon()

            logger.debug(f'Collecting data from: {w}')
            data[w.field_name] = w.collect()

        if errors:
            ui.notify(f"Исправьте ошибки в форме: {self.title}")
            raise FormError(form_name=self.title)

        return data

    def render_json_viewer_dialog(self) -> None:
        JsonDialog(model=self.build_model()).render()

    def build_model(self) -> T:
        """Собирать данные введенные в виджетах с помощью метода .collect_date()
        и создать BaseModel объект. Не игнорирует ошибки валидации в виджетах"""
        data = self.collect_data()
        try:
            return self.model(**data)
        except ValidationError as e:
            e: ValidationError
            for err in e.errors():

                err_msg = tr.translate(
                    code=err['type'], ctx=err.get('ctx'), default=err.get('msg')
                )
                w = self.widgets.get(err['loc'][0])
                if w:
                    w.view_error(err_msg)
                    w.element.error = err_msg

            ui.notify(f"Исправьте ошибки в форме: {self.title}")
            raise FormError(form_name=self.title)

    def render_without_wrapper(self) -> None:
        self.header = Header(
            title=self.title,
            description=self.description,
            bg_color=self.header_bg_color,
            parent_card=self.body_element,
            is_nested=self._is_nested,
            is_nullable=self._is_nullable,
        )
        self.header.render()

        Body(
            widgets=list(self.widgets.values()),
        ).render()

        if not self._is_nested:
            Footer(
                model=self.model,
                on_submit=self.on_submit,
                on_collect=self.build_model,
                buttons=list(self.buttons.values()),
            ).render()

    @overload
    def render(self) -> Card: ...

    @overload
    def render(self, wrap: Literal['card'] = 'card') -> Card: ...

    @overload
    def render(self, wrap: Literal['dialog'] = 'dialog') -> Dialog: ...

    def render(self, wrap: Literal['dialog', 'card'] = 'card') -> Element:
        """Render and wrap the form UI."""

        logger.debug(f'Rendering form "{self.model.__name__} wrap={wrap}"')

        # --- DIALOG ---
        if wrap == 'dialog':
            with ui.dialog() as self.dialog:
                with ui.card().classes(self.wrapper_classes) as self.body_element:
                    self.render_without_wrapper()

            self._is_rendered = True
            return self.dialog

        # --- CARD  ---
        if wrap == 'card':
            with ui.card().classes(self.wrapper_classes) as self.body_element:
                self.render_without_wrapper()

            self._is_rendered = True
            return self.body_element

        raise ValueError(f'Invalid wrap: {wrap}')

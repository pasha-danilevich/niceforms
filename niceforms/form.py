"""
Universal Pydantic model form renderer for NiceGUI.

This module provides a dynamic form generator that automatically creates
UI forms from Pydantic models with support for nested models, validation,
and various input types.
"""

import inspect
from datetime import date, datetime, time
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    get_type_hints,
)

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.button import Button
from nicegui.elements.mixins.label_element import LabelElement
from pydantic import BaseModel, ValidationError
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from ui import Header
from utils import TypeProcessor
from utils.constants import *
from widgets.factory import WidgetFactory

# Type variables
M = TypeVar("M", bound=BaseModel)
T = TypeVar("T")





class FieldWidgetFactory:
    """Factory for creating form widgets based on field types."""

    def __init__(self, form: "TheBaseModelForm") -> None:
        """Initialize the widget factory.

        Args:
            form: Reference to the parent form
        """
        self.form = form

    def create_widget(
        self,
        field_name: str,
        field_type: Type,
        field_info: FieldInfo,
    ) -> Optional[LabelElement]:
        """Create a widget based on field type.

        Args:
            field_name: Name of the field
            field_type: Type of the field
            field_info: Pydantic field information

        Returns:
            Created widget or None if widget is nested
        """

        type_hints = get_type_hints(self.form.model)
        actual_type = type_hints.get(field_name, field_type)

        is_optional = TypeProcessor.is_optional_type(actual_type)
        base_type = (
            TypeProcessor.get_base_type(actual_type) if is_optional else actual_type
        )

        if inspect.isclass(base_type) and issubclass(base_type, Enum):
            return self._create_enum_widget(
                field_name, base_type, field_info, is_optional
            )

        if hasattr(base_type, "model_dump"):  # Nested model
            return self._create_nested_widget(field_name, base_type)  # type: ignore

        return self._create_basic_widget(field_name, base_type, field_info, is_optional)

    def _create_enum_widget(
        self,
        field_name: str,
        enum_type: Type[Enum],
        field_info: FieldInfo,
        is_optional: bool,
    ) -> None:
        """Create a dropdown widget for enum fields.

        Args:
            field_name: Name of the field
            enum_type: Enum class
            field_info: Pydantic field information
            is_optional: Whether the field is optional
        """
        metadata = self._extract_field_metadata(field_name, field_info)
        options = [(item.value, item.name) for item in enum_type]
        select_options = {value: label for value, label in options}
        select_options[NULL_OPTION_VALUE] = NULL_OPTION_LABEL  # type: ignore

        with ui.column().classes("w-full gap-1"):
            self._create_field_header(field_name, metadata, is_optional)

            if metadata.get("tooltip"):
                ui.label(metadata["tooltip"]).classes("text-xs text-gray-500 -mt-1")

            widget = (
                ui.select(options=select_options, value=NULL_OPTION_VALUE)
                .props("outlined dense")
                .classes("w-full")
                .on(
                    "update:model-value",
                    lambda e: self.form.update_none_button_state(field_name, widget),
                )
            )

            self.form.fields[field_name] = widget
            self._create_none_button(field_name, widget, is_optional)
            self._create_error_container(field_name)

    def _create_nested_widget(
        self, field_name: str, model_type: Type[BaseModel]
    ) -> None:
        """Create a nested form widget.

        Args:
            field_name: Name of the field
            model_type: Nested model class
        """
        with ui.expansion(
            field_name.replace("_", " ").title(), icon="expand_more"
        ).classes("w-full").props("dense"):
            nested_form = TheBaseModelForm(model_type)
            nested_form._is_nested = True
            nested_form.render()
            self.form.fields[field_name] = nested_form

    def _create_basic_widget(
        self,
        field_name: str,
        base_type: Type,
        field_info: FieldInfo,
        is_optional: bool,
    ) -> None:
        """Create a basic input widget.

        Args:
            field_name: Name of the field
            base_type: Base type of the field
            field_info: Pydantic field information
            is_optional: Whether the field is optional
        """
        metadata = self._extract_field_metadata(field_name, field_info)
        label = metadata.get("label", field_name.replace("_", " ").title())

        with ui.column().classes("w-full gap-1"):
            self._create_field_header(field_name, metadata, is_optional, base_type)

            if metadata.get("tooltip"):
                ui.label(metadata["tooltip"]).classes("text-xs text-gray-500 -mt-1")

            widget = self._create_widget_by_type(field_name, base_type, metadata, label)
            self.form.fields[field_name] = widget
            self._create_none_button(field_name, widget, is_optional)
            self._create_error_container(field_name)

    def _extract_field_metadata(
        self,
        field_name: str,
        field_info: FieldInfo,
    ) -> Dict[str, Any]:
        """Extract metadata from field info.

        Args:
            field_name: Name of the field
            field_info: Pydantic field information

        Returns:
            Dictionary with field metadata
        """
        label: str = field_info.title or field_name.replace("_", " ").title()

        metadata: Dict[str, Any] = {
            "label": label,
            "placeholder": field_info.description or f'Введите {label.lower()}',
            "tooltip": getattr(field_info, "extra", {}).get("description", ""),
        }

        # Extract constraints
        for attr in ["gt", "lt", "ge", "le"]:
            if hasattr(field_info, attr):
                metadata[attr] = getattr(field_info, attr)

        default_value = self._get_default_value(field_info)
        if default_value is not None:
            metadata["default_value"] = default_value
            metadata["default_display"] = self._format_default_value(default_value)

        return metadata

    @staticmethod
    def _get_default_value(field_info: FieldInfo) -> Any:
        """Get default value from field info.

        Args:
            field_info: Pydantic field information

        Returns:
            Default value or None
        """
        if (
            hasattr(field_info, "default")
            and field_info.default is not PydanticUndefined
        ):
            return field_info.default
        return None

    @staticmethod
    def _format_default_value(value: Any) -> str:
        """Format default value for display.

        Args:
            value: Default value to format

        Returns:
            Formatted string
        """
        if isinstance(value, Enum):
            return f"default={value.value}"
        return f"default={value}"

    def _create_field_header(
        self,
        field_name: str,
        metadata: Dict[str, Any],
        is_optional: bool,
        field_type: Optional[Type] = None,
    ) -> None:
        """Create field header with label and optional elements.

        Args:
            field_name: Name of the field
            metadata: Field metadata
            is_optional: Whether the field is optional
            field_type: Type of the field (optional)
        """
        label = metadata.get("label", field_name.replace("_", " ").title())
        is_required = not is_optional and metadata.get("default_value") is None

        with ui.row().classes("w-full justify-between items-baseline"):
            with ui.row().classes("items-baseline gap-1"):
                ui.label(f"{label}{' *' if is_required else ''}").classes(
                    "text-sm font-medium text-gray-700"
                )

                if field_type:
                    type_name = (
                        field_type.__name__
                        if hasattr(field_type, "__name__")
                        else str(field_type)
                    )
                    ui.label(f"[{type_name}]").classes(
                        "text-xs font-normal text-gray-400 opacity-75"
                    )

            if is_optional:
                self.form.none_buttons[field_name] = (
                    ui.button("Set None")
                    .props("flat dense size=sm")
                    .classes("bg-gray-100 hover:bg-gray-200")
                )

    def _create_widget_by_type(
        self,
        field_name: str,
        base_type: Type,
        metadata: Dict[str, Any],
        label: str,
    ) -> Element:
        """Create widget based on type.

        Args:
            field_name: Name of the field
            base_type: Type of the field
            metadata: Field metadata
            label: Field label

        Returns:
            Created widget
        """
        placeholder = metadata.get(
            "placeholder", self._get_default_placeholder(base_type, label)
        )

        if metadata.get("default_value") and metadata.get("default_display"):
            placeholder = f"{placeholder} ({metadata['default_display']})"

        widget_creators = {
            str: (
                lambda: ui.input(placeholder=placeholder)
                .props("outlined dense")
                .classes("w-full")
            ),
            int: (
                lambda: ui.number(
                    placeholder=placeholder,
                    min=metadata.get("ge") or metadata.get("gt"),
                    max=metadata.get("le") or metadata.get("lt"),
                    format="%d",
                )
                .props("outlined dense")
                .classes("w-full")
            ),
            float: (
                lambda: ui.number(
                    placeholder=placeholder,
                    min=metadata.get("ge") or metadata.get("gt"),
                    max=metadata.get("le") or metadata.get("lt"),
                    precision=2,
                )
                .props("outlined dense")
                .classes("w-full")
            ),
            bool: lambda: ui.checkbox(text=label),
            datetime: (
                lambda: ui.input(placeholder=placeholder)
                .props("outlined dense type=datetime-local")
                .classes("w-full")
            ),
            date: (
                lambda: ui.input(placeholder=placeholder)
                .props("outlined dense type=date")
                .classes("w-full")
            ),
            time: (
                lambda: ui.input(placeholder=placeholder)
                .props("outlined dense type=time")
                .classes("w-full")
            ),
        }

        if base_type in widget_creators:
            widget = widget_creators[base_type]()  # type: ignore
        elif TypeProcessor.is_list_type(base_type):
            widget = (
                ui.textarea(placeholder=placeholder)
                .props("outlined dense")
                .classes("w-full")
            )
        else:
            widget = (
                ui.input(placeholder=placeholder)
                .props("outlined dense")
                .classes("w-full")
            )

        widget.on(
            "update:model-value",
            lambda e: self.form.update_none_button_state(field_name, widget),
        )

        return widget

    @staticmethod
    def _get_default_placeholder(base_type: Type, label: str) -> str:
        """Get default placeholder based on type.

        Args:
            base_type: Type of the field
            label: Field label

        Returns:
            Default placeholder text
        """
        placeholders = {
            str: f"Введите {label.lower()}",
            int: f"Введите {label.lower()}",
            float: f"Введите {label.lower()}",
            bool: label,
            datetime: "Выберите дату и время",
            date: "Выберите дату",
            time: "Выберите время",
        }

        if TypeProcessor.is_list_type(base_type):
            return "Введите значения, каждое с новой строки"

        return placeholders.get(base_type, f"Введите {label.lower()}")  # type: ignore

    def _create_none_button(
        self,
        field_name: str,
        widget: Element,
        is_optional: bool,
    ) -> None:
        """Create None button for optional fields.

        Args:
            field_name: Name of the field
            widget: Field widget
            is_optional: Whether the field is optional
        """
        if not is_optional or field_name not in self.form.none_buttons:
            return

        def set_none() -> None:
            if isinstance(widget, ui.checkbox):
                widget.value = False
            elif hasattr(widget, "value"):
                widget.value = None

            self.form.none_buttons[field_name].props("color=positive")
            self.form.none_buttons[field_name].set_text("✓ None")

        self.form.none_buttons[field_name].on_click(set_none)

    def _create_error_container(self, field_name: str) -> None:
        """Create error container for field validation.

        Args:
            field_name: Name of the field
        """
        error_container = (
            ui.label("")
            .classes("text-xs text-red-500 hidden")
            .bind_visibility_from(
                self.form.field_states,
                field_name,
                lambda x: bool(x.get("error", "")),
            )
        )

        self.form.field_states[field_name] = {
            "error": "",
            "container": error_container,
        }


class TheBaseModelForm(Generic[M]):
    """Universal form generator for Pydantic models."""

    def __init__(
        self,
        model: Type[BaseModel],
        submit_callback: Optional[Callable[[M], Any]] = None,
        title: Optional[str] = None,
        widget_factory: type[WidgetFactory] = WidgetFactory,
    ) -> None:
        """Initialize universal form.

        Args:
            model: Pydantic model class
            submit_callback: Callback function for form submission
            title: Form title (if None, uses model name)
        """
        self.model = model
        self.submit_callback = submit_callback
        self.title = title or model.__name__

        self.fields: Dict[str, Union[Element, TheBaseModelForm]] = {}
        self.none_buttons: Dict[str, Button] = {}
        self.form_data: Dict[str, Any] = {}
        self.field_states: Dict[str, Dict[str, Any]] = {}

        self._success_message: Optional[Element] = None
        self._error_container: Optional[Element] = None
        self._submit_button: Optional[Button] = None
        self._write_to_form_button: Optional[Button] = None

        self._is_nested: bool = False
        self._is_write_to_form: bool = False

        self.widget_factory = widget_factory(model_fields=model.model_fields())

    def _write_to_form(self) -> None:
        """Handle write to form action for nested forms."""
        if not self._is_nested:
            raise ValueError("Объект не является вложенным")

        self._is_write_to_form = True

        if not self._write_to_form_button:
            raise ValueError("Кнопка не записана в переменную")

        self._write_to_form_button.disable()

    def update_none_button_state(self, field_name: str, widget: Element) -> None:
        """Update None button state based on widget value.

        Args:
            field_name: Name of the field
            widget: Field widget
        """
        if field_name not in self.none_buttons:
            return

        if hasattr(widget, "value"):
            is_none = widget.value is None or widget.value == ""

            if isinstance(widget, ui.checkbox):
                is_none = False  # Checkboxes don't use None values

            button = self.none_buttons[field_name]
            if is_none:
                button.props("color=positive")
                button.set_text("✓ None")
            else:
                button.props("color=primary")
                button.set_text("Set None")

    def get_form_data(self) -> Dict[str, Any]:
        """Get data from form widgets.

        Returns:
            Dictionary with form data
        """
        data: Dict[str, Any] = {}

        for field_name, widget in self.fields.items():
            if isinstance(widget, TheBaseModelForm):
                if widget._is_write_to_form:
                    data[field_name] = widget.get_form_data()
            elif isinstance(widget, ui.textarea):
                data[field_name] = self._process_textarea_value(widget.value)
            elif isinstance(widget, ui.checkbox):
                data[field_name] = widget.value
            elif isinstance(widget, ui.select):
                if widget.value is not None:
                    data[field_name] = widget.value
            elif isinstance(widget, ui.number):
                if widget.value is not None:
                    data[field_name] = int(widget.value)

            elif hasattr(widget, "value") and widget.value != "":  # type: ignore
                data[field_name] = widget.value

        return data

    @staticmethod
    def _process_textarea_value(value: Optional[str]) -> Optional[List[str]]:
        """Process textarea value into list of strings.

        Args:
            value: Textarea value

        Returns:
            List of strings or None
        """
        if value:
            return [line.strip() for line in value.split("\n") if line.strip()]
        return None

    def validate_form(self) -> Optional[M]:
        """Validate form data and create model instance.

        Returns:
            Validated model instance or None if validation fails
        """
        try:
            form_data = self.get_form_data()

            instance = self.model(**form_data)
            self.clear_field_errors()
            return instance
        except ValidationError as e:
            self.show_errors(e)
            return None

    def clear_field_errors(self) -> None:
        """Clear all field errors."""
        for state in self.field_states.values():
            state["error"] = ""
            if "container" in state:
                state["container"].set_text("")

    def show_errors(self, validation_error: ValidationError) -> None:
        """Display validation errors.

        Args:
            validation_error: Validation error object
        """
        if self._error_container:
            self._error_container.clear()

        for field_name in self.field_states:
            self.field_states[field_name]["error"] = ""

        field_errors = self._collect_field_errors(validation_error)

        for field_name, errors in field_errors.items():
            if field_name in self.field_states:
                error_text = "; ".join(errors)
                self.field_states[field_name]["error"] = error_text
                if "container" in self.field_states[field_name]:
                    self.field_states[field_name]["container"].set_text(error_text)
                    self.field_states[field_name]["container"].classes(
                        remove="hidden", add="block"
                    )

        self._show_form_errors(validation_error)

    @staticmethod
    def _collect_field_errors(
        validation_error: ValidationError,
    ) -> Dict[str, List[str]]:
        """Collect errors from validation error object.

        Args:
            validation_error: Validation error object

        Returns:
            Dictionary mapping field names to error messages
        """
        field_errors: Dict[str, List[str]] = {}

        for error in validation_error.errors():
            field = error["loc"][0] if error["loc"] else "form"
            msg = error["msg"]
            field_errors.setdefault(field, []).append(msg)

        return field_errors

    def _show_form_errors(self, validation_error: ValidationError) -> None:
        """Display form-level errors.

        Args:
            validation_error: Validation error object
        """
        self._error_container = ui.column().classes("w-full gap-2 mt-4")

        with self._error_container:
            with ui.card().classes(
                f"{ERROR_BACKGROUND_COLOR} {ERROR_BORDER_COLOR} border-2"
            ).style("width: -webkit-fill-available;"):
                with ui.row():
                    ui.icon("error").classes("text-red-500 text-lg")
                    ui.label("Ошибки при заполнении формы").classes(
                        "text-red-700 font-semibold"
                    )

                ui.separator().classes("bg-red-200")

                for error in validation_error.errors():
                    field = " → ".join(str(loc) for loc in error["loc"])
                    msg = error["msg"]
                    ui.label(f"• {field}: {msg}").classes("text-red-600 text-sm")

    async def submit(self) -> bool:
        """Handle form submission.

        Returns:
            True if submission successful, False otherwise
        """
        if not self._submit_button:
            return False

        original_text = self._submit_button.text
        self._submit_button.disable()
        self._submit_button.set_text("Отправка...")

        try:
            validated_data = self.validate_form()

            if validated_data is not None:
                self.form_data = validated_data.model_dump()

                print(f"Submitted form data: {self.form_data}")

                if self.submit_callback:
                    if inspect.iscoroutinefunction(self.submit_callback):
                        await self.submit_callback(validated_data)
                    else:
                        self.submit_callback(validated_data)

                self._show_success_message()
                return True

        except Exception as e:
            ui.notify(f"Ошибка при отправке: {str(e)}", type="negative")
            raise
        finally:
            self._submit_button.enable()
            self._submit_button.set_text(original_text)

        return False

    def _show_success_message(self) -> None:
        """Display success message after form submission."""

        if self._error_container:
            try:
                self._error_container.delete()
            except ValueError:
                self._error_container = None

        if self._success_message:
            self._success_message.delete()
        else:
            self._success_message = ui.column().classes("w-full mt-4")

        with self._success_message:
            with ui.card().classes(
                f"{SUCCESS_BACKGROUND_COLOR} {SUCCESS_BORDER_COLOR} border-2"
            ):
                ui.icon("check_circle").classes("text-green-500 text-lg")
                ui.label("Форма успешно отправлена!").classes(
                    "text-green-700 font-semibold"
                )
                ui.label("Данные валидированы и обработаны").classes(
                    "text-green-600 text-sm"
                )

    def render(self) -> None:
        """Render the form UI."""
        schema = self.model.model_json_schema()
        widgets = self.widget_factory.build()
        # properties = schema.get("properties", {})

        with ui.card().classes(
            f"w-full {DEFAULT_FORM_WIDTH} mx-auto shadow-lg rounded-xl overflow-hidden"
        ):

            Header(title=self.title, description=schema.get('description')).render()
            self._render_body(properties)
            self._render_footer_buttons()

    def _render_header(self, schema: Dict[str, Any]) -> None:
        """Render form header.

        Args:
            schema: Model JSON schema
        """
        with ui.column().classes(f"w-full {PRIMARY_COLOR_GRADIENT} {DEFAULT_PADDING}  rounded-lg"):
            ui.label(self.title).classes("text-2xl font-bold text-white")

            description = schema.get("description")
            if description:
                ui.label(description).classes("text-blue-100 mt-2")

    def _render_body(self, properties: Dict[str, Any]) -> None:
        """Render form body with fields.

        Args:
            properties: Model properties from schema
        """
        with ui.column().classes(f"w-full {DEFAULT_PADDING} space-y-6"):
            for field_name, _ in properties.items():
                field_info = self.model.model_fields[field_name]
                field_type = field_info.annotation
                self.widget_factory.create_widget(field_name, field_type, field_info)

    def _render_footer_buttons(self) -> None:
        """Render form footer with buttons."""
        with ui.row().classes("w-full justify-end gap-3"):
            ui.button("Очистить", on_click=self.clear_form).props(
                "outlined flat"
            ).classes("px-6 py-2")
            ui.button("Показать json", on_click=self.render_json_viewer_dialog).props(
                "outlined flat"
            ).classes("px-6 py-2")

            if self._is_nested:
                self._write_to_form_button = (
                    ui.button("Сохранить в форму", on_click=self._write_to_form)
                    .props("unelevated")
                    .classes(f"{PRIMARY_COLOR_GRADIENT} text-white px-8 py-2")
                )
            else:
                self._submit_button = (
                    ui.button("Отправить", on_click=self.submit, icon="send")
                    .props("unelevated")
                    .classes(f"{PRIMARY_COLOR_GRADIENT} text-white px-8 py-2")
                )

    def clear_form(self) -> None:
        """Clear form values and reset state."""
        for field_name, widget in self.fields.items():
            if isinstance(widget, TheBaseModelForm):
                widget.clear_form()
            elif hasattr(widget, "value"):
                widget.value = None if not isinstance(widget, ui.checkbox) else False

        for button in self.none_buttons.values():
            button.props("color=primary")
            button.set_text("Set None")

        if self._write_to_form_button:
            self._write_to_form_button.enable()

        if self._error_container:
            try:
                self._error_container.delete()
            except ValueError:
                self._error_container = None

        if self._success_message:
            self._success_message.delete()

        self.clear_field_errors()
        ui.notify(f"Форма {self.title} очищена", type="info")

    def render_json_viewer_dialog(self) -> None:
        obj = self.validate_form()
        if obj is None:
            return

        json_data = {'content': {'json': obj.model_dump()}}

        with ui.dialog() as dialog, ui.card():
            ui.label('Результирующий JSON объект').classes('text-h5 font-bold')
            ui.label('(только чтение)')

            # ui.json автоматически красиво форматирует JSON
            ui.json_editor(json_data).classes('w-full')

            with ui.row().classes('justify-end w-full mt-4'):
                ui.button('Close', on_click=dialog.close).props('flat')

        dialog.open()

import datetime
import logging
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from .widget import BaseWidget
from .widget.bool import BoolWidget
from .widget.datetime import DateTimeWidget, DateWidget
from .widget.enum import EnumWidget
from .widget.float import FloatWidget
from .widget.integer import IntegerWidget
from .widget.list import ListWidget
from .widget.list_basemodel import ListBaseModelWidget
from .widget.string import StringWidget
from .widget.unknown_type import UnknownTypeWidget
from .utils import is_enum_type, is_list_basemodel_type, normalize_type

logger = logging.getLogger(__name__)


class WidgetFactory:
    def __init__(self) -> None:
        self._widgets: dict[type, type[BaseWidget]] = {
            str: StringWidget,
            int: IntegerWidget,
            int | None: IntegerWidget,
            Enum: EnumWidget,
            bool: BoolWidget,
            float: FloatWidget,
            list[str]: ListWidget,
            List[str]: ListWidget,
            list[int]: ListWidget,
            List[int]: ListWidget,
            datetime.date: DateWidget,
            datetime.datetime: DateTimeWidget,
            list[BaseModel]: ListBaseModelWidget,
        }

    def insert_new_widget(
        self, field_type: type, widget_type: type[BaseWidget]
    ) -> None:
        assert issubclass(widget_type, BaseWidget), 'Widget must be a subclass of BaseWidget'

        self._widgets[field_type] = widget_type

    # def build(
    #     self,
    #     model_fields: dict[str, FieldInfo],
    #     view_annotation_type: bool,
    #     custom_field_widget: Optional[dict[str, type[BaseWidget]]],
    # ) -> list[BaseWidget]:
    #     widgets: list[BaseWidget] = []
    #
    #     for field_name, field_type in model_fields.items():
    #         normalized_type = normalize_type(field_type.annotation)
    #
    #         widget = self._widgets.get(field_type.annotation)
    #
    #         if not widget:
    #             widget = self._widgets.get(normalized_type.origin_type)
    #
    #         if is_enum_type(normalized_type.origin_type):
    #             widget = self._widgets.get(Enum)
    #
    #         if is_list_basemodel_type(normalized_type.origin_type):
    #             widget = self._widgets.get(list[BaseModel])
    #
    #         if custom_field_widget:
    #             widget = custom_field_widget.get(field_name, widget)
    #
    #         if widget is None:
    #             logger.warning(
    #                 f'No widget for field "{field_name}". Type {field_type.annotation}. Creating default <UnknownTypeWidget>'
    #             )
    #             widget = UnknownTypeWidget
    #
    #         logger.debug(f"Adding widget: {widget.__name__}")
    #         widgets.append(
    #             widget(
    #                 field_info=field_type,
    #                 field_name=field_name,
    #                 normalized_type=normalized_type,
    #                 view_annotation_type=view_annotation_type,
    #                 custom_field_widget=custom_field_widget,
    #             )
    #         )
    #
    #     return widgets

    @staticmethod
    def extract_custom_field_widget(data: dict[str, type[BaseWidget]], model_name: str) -> dict[str, type[BaseWidget]]:
        """
        Extract fields that belong to a specific model from the input dictionary.

        Args:
            data: Dictionary with keys in format '{model_name}:{field_name}'
            model_name: The name of the model to extract fields for

        Returns:
            Dictionary with field names as keys and their values, without the model prefix
        """
        prefix = f"{model_name}:"
        result = {}

        for key, value in data.items():
            if key.startswith(prefix):
                field_name = key[len(prefix) :]  # Remove the prefix
                result[field_name] = value

        return result

    def ensure_widget_type(
        self,
        field_name: str,
        field_info: FieldInfo,
        model_name: str,
        custom_field_widget: Optional[dict[str, type[BaseWidget]]],
    ) -> type[BaseWidget]:
        normalized_type = normalize_type(field_info.annotation)

        widget_type = self._widgets.get(field_info.annotation)

        if not widget_type:
            widget_type = self._widgets.get(normalized_type.origin_type)

        if is_enum_type(normalized_type.origin_type):
            widget_type = self._widgets.get(Enum)

        if is_list_basemodel_type(normalized_type.origin_type):
            widget_type = self._widgets.get(list[BaseModel])

        if custom_field_widget:
            extracted = self.extract_custom_field_widget(data=custom_field_widget, model_name=model_name)
            widget_type = extracted.get(field_name, widget_type)

        if widget_type is None:
            logger.warning(
                f'No widget for field "{field_name}". Type {field_info.annotation}. Creating default <UnknownTypeWidget>'
            )
            widget_type = UnknownTypeWidget

        return widget_type

    def build(
        self,
        field_name: str,
        field_info: FieldInfo,
        model_name: str,
        custom_field_widget: Optional[dict[str, type[BaseWidget]]],
    ) -> BaseWidget:
        normalized_type = normalize_type(field_info.annotation)

        return self.ensure_widget_type(
            field_name=field_name,
            field_info=field_info,
            model_name=model_name,
            custom_field_widget=custom_field_widget,
        )(
            field_info=field_info,
            field_name=field_name,
            normalized_type=normalized_type,
        )

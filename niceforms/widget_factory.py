import datetime
import logging
from enum import Enum
from typing import List

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from utils import is_enum_type, is_list_basemodel_type, normalize_type
from widget import BaseWidget
from widget.bool import BoolWidget
from widget.datetime import DateTimeWidget, DateWidget
from widget.enum import EnumWidget
from widget.float import FloatWidget
from widget.integer import IntegerWidget
from widget.list import ListWidget
from widget.list_basemodel import ListBaseModelWidget
from widget.string import StringWidget
from widget.unknown_type import UnknownTypeWidget

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
        self._widgets[field_type] = widget_type

    def build(
        self, model_fields: dict[str, FieldInfo], view_annotation_type: bool
    ) -> list[BaseWidget]:
        widgets: list[BaseWidget] = []

        for field_name, field_type in model_fields.items():
            normalized_type = normalize_type(field_type.annotation)
            try:
                widget = self._widgets[field_type.annotation]
            except KeyError:
                widget = self._widgets.get(normalized_type.origin_type)

            if is_enum_type(normalized_type.origin_type):
                widget = self._widgets[Enum]

            if is_list_basemodel_type(normalized_type.origin_type):
                widget = self._widgets[list[BaseModel]]

            if widget is None:
                logger.warning(
                    f'No widget for field "{field_name}". Type {field_type.annotation}. Creating default <UnknownTypeWidget>'
                )
                widget = UnknownTypeWidget

            logger.debug(f"Adding widget: {widget.__name__}")
            widgets.append(
                widget(
                    field_info=field_type,
                    field_name=field_name,
                    normalized_type=normalized_type,
                    view_annotation_type=view_annotation_type,
                )
            )

        return widgets

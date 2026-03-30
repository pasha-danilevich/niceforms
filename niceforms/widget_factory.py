import datetime
import logging
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from .utils import (
    is_enum_type,
    is_list_basemodel_type,
    normalize_type,
    is_basemodel_type,
)
from .widget import BaseWidget
from .widget.bool import BoolWidget
from .widget.datetime import DateTimeWidget, DateWidget
from .widget.enum import EnumWidget
from .widget.float import FloatWidget
from .widget.integer import IntegerWidget
from .widget.list import ListWidget
from .widget.list_basemodel import ListBaseModelWidget
from .widget.nested import NestedWidget
from .widget.string import StringWidget
from .widget.unknown_type import UnknownTypeWidget

logger = logging.getLogger(__name__)


class WidgetFactory:
    widgets: dict[type, type[BaseWidget]] = {
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
        BaseModel: NestedWidget,
    }

    def __init__(self, model: type[BaseModel], view_annotation: bool) -> None:
        self.model = model
        self.view_annotation_type = view_annotation
        self.fields: dict[str, FieldInfo] = self.model.model_fields  # type: ignore # field_name: FieldInfo

    def insert_new_widget(
        self, field_type: type, widget_type: type[BaseWidget]
    ) -> None:
        assert issubclass(
            widget_type, BaseWidget
        ), 'Widget must be a subclass of BaseWidget'

        self.widgets[field_type] = widget_type

    def ensure_widget_type(
        self,
        field_name: str,
        field_info: FieldInfo,
    ) -> type[BaseWidget]:
        normalized_type = normalize_type(field_info.annotation)

        widget_type = self.widgets.get(field_info.annotation)

        if not widget_type:
            widget_type = self.widgets.get(normalized_type.origin_type)

        if is_enum_type(normalized_type.origin_type):
            widget_type = self.widgets.get(Enum)

        if is_list_basemodel_type(normalized_type.origin_type):
            widget_type = self.widgets.get(list[BaseModel])

        if is_basemodel_type(normalized_type.origin_type):
            widget_type = self.widgets.get(BaseModel)

        if widget_type is None:
            logger.warning(
                f'No widget for field "{field_name}". Type {field_info.annotation}. Creating default <UnknownTypeWidget>'
            )
            widget_type = UnknownTypeWidget

        return widget_type

    def build(
        self,
        field_name: str,
        widget_type: Optional[type[BaseWidget]] = None,
        kwargs: Optional[dict] = None,
    ) -> BaseWidget:
        kwargs = kwargs or {}
        field_info = self.fields[field_name]

        if widget_type:
            return widget_type(
                field_info=field_info,
                field_name=field_name,
                view_annotation=self.view_annotation_type,
                **kwargs,
            )

        return self.ensure_widget_type(
            field_name,
            field_info,
        )(
            field_info=field_info,
            field_name=field_name,
            view_annotation=self.view_annotation_type,
            **kwargs,
        )

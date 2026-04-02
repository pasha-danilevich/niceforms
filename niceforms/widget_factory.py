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


from collections import defaultdict
from typing import get_origin, get_args


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

    _base_widgets = widgets.copy()
    _insert_history: list[tuple[type, type[BaseWidget]]] = []

    def __init__(self, model: type[BaseModel], view_annotation: bool) -> None:
        self.model = model
        self.view_annotation_type = view_annotation
        self.fields: dict[str, FieldInfo] = self.model.model_fields  # type: ignore # field_name: FieldInfo

    @classmethod
    def insert_new_widget(
        cls, field_type: type, widget_type: type[BaseWidget]
    ) -> None:
        assert issubclass(
            widget_type, BaseWidget
        ), 'Widget must be a subclass of BaseWidget'
        logger.info(f'Inserting new widget type {widget_type}')
        cls.widgets[field_type] = widget_type

    @classmethod
    def register_widget(cls, field_type: type, widget: type[BaseWidget]) -> None:
        """Добавляет новый виджет и пишет в историю."""
        cls.widgets[field_type] = widget
        cls._insert_history.append((field_type, widget))

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


    @classmethod
    def _type_name(cls, t: type) -> str:
        return repr(t)

    @classmethod
    def print_widget_registry(cls) -> None:
        # --- подготовка ---
        rows: list[tuple[str, str, str]] = []

        for field_type, widget in cls.widgets.items():
            marker = " "

            if field_type not in cls._base_widgets:
                marker = "+"
            elif cls._base_widgets.get(field_type) != widget:
                marker = "~"

            rows.append(
                (
                    marker,
                    cls._type_name(field_type),
                    widget.__name__,
                )
            )

        # считаем ширину колонок
        type_width = max(len(r[1]) for r in rows) if rows else 0
        widget_width = max(len(r[2]) for r in rows) if rows else 0

        # --- пользовательские ---
        if cls._insert_history:
            print("\nUser-added widgets")
            print("-" * 60)

            for field_type, widget in cls._insert_history:
                type_name = cls._type_name(field_type)
                print(f"  + {type_name:<{type_width}}  ->  {widget.__name__}")

        # --- текущие ---
        print("\nCurrent widgets")
        print("-" * 60)

        for marker, type_name, widget_name in sorted(rows, key=lambda x: x[1]):
            print(
                f"{marker} {type_name:<{type_width}}  ->  {widget_name:<{widget_width}}"
            )

        print("\n" + "=" * 60 + "\n")
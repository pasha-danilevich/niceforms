from abc import ABC

from pydantic.fields import FieldInfo

from ui.components import UIComponent
from widgets.impl import StrWidget


class Widget(UIComponent, ABC):
    def __init__(self, field: FieldInfo):
        self.field = field


class WidgetFactory:
    def __init__(self, model_fields: dict[str, FieldInfo]) -> None:
        self.model_fields = model_fields
        self._widgets: dict[type, type[Widget]] = {
            str: StrWidget,
        }

    def insert_new_widget(self, field_type: type, widget_type: type[Widget]) -> None:
        self._widgets[field_type] = widget_type

    def build(self) -> list[Widget]:
        widgets = []

        for field_name, field_type in self.model_fields.items():
            widget = self._widgets[field_type.annotation]
            widgets.append(widget)

        return widgets
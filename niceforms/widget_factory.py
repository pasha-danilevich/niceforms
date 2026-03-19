import logging

from pydantic.fields import FieldInfo

from utils import normalize_type
from widget.string import StringWidget
from widget import BaseWidget

logger = logging.getLogger(__name__)



class WidgetFactory:
    def __init__(self) -> None:
        self._widgets: dict[type, type[BaseWidget]] = {
            str: StringWidget,
        }

    def insert_new_widget(self, field_type: type, widget_type: type[BaseWidget]) -> None:
        self._widgets[field_type] = widget_type

    def build(self, model_fields: dict[str, FieldInfo]) -> list[BaseWidget]:
        widgets: list[BaseWidget] = []


        for field_name, field_type in model_fields.items():

            try:
                widget = self._widgets[field_type.annotation]
            except KeyError:
                widget = self._widgets.get(normalize_type(field_type.annotation))


            if widget is None:
                logger.warning(f'No widget for field "{field_name}". Type {field_type.annotation}')
                continue

            widgets.append(widget(field_info=field_type, field_name=field_name))


        return widgets
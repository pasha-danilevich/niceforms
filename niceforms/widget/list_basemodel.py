from typing import Optional

from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement
from pydantic import BaseModel

from niceforms.widget import BaseWidget


class ListBaseModelWidget(BaseWidget):

    def collect(self) -> Optional[list[BaseModel]]:
        pass

    def render(self) -> ValueElement:
        return ValueElement(value='')

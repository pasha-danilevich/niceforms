from typing import Optional

from nicegui.elements.mixins.value_element import ValueElement
from pydantic import BaseModel
from pyexpat import model

from niceforms import BaseWidget
from utils import extract_inner_type
from .component import ListComponent


class ListBaseModelWidget(BaseWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.component: Optional[ListComponent[BaseModel]] = None

    def collect(self) -> Optional[list[BaseModel]]:
        if len(self.component.storage) == 0 and self.normalized_type.is_nullable:
            return None

        return self.component.storage

    @staticmethod
    def get_record_title(model: BaseModel) -> str:
        return model.name

    def render(self) -> ValueElement:
        model_type = extract_inner_type(self.normalized_type.origin_type)

        self.component = ListComponent(
            storage=self.default_value if self.default_value else [],
            record_title_getter=self.get_record_title,
            model=model_type,
        )
        self.component.render()
        return ValueElement(value='')

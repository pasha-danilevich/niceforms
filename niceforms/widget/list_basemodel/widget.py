from typing import Optional, Any

from nicegui.element import Element
from nicegui.elements.mixins.value_element import ValueElement
from pydantic import BaseModel

from niceforms import BaseWidget
from utils import extract_inner_type
from .component import ListComponent


class ListBaseModelWidget(BaseWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.model_type: type[BaseModel]
        self.component: Optional[ListComponent[BaseModel]] = None

    def fill(self, data: Optional[list[dict[str, Any] | BaseModel]]) -> None:
        if data is None:
            self.component.storage = []
            return

        result = []
        for item in data:
            if isinstance(item, BaseModel):
                # Если это уже модель, используем её напрямую
                result.append(item)
            else:
                # Если это словарь, создаём модель
                result.append(self.model_type(**item))

        self.component.storage = result
        self.component.refresh_list()

    def validate(self) -> Optional[str]:
        if not self.normalized_type.is_nullable and self.component.storage is None:
            return 'Не должно быть пусто'
        return None

    def clear(self) -> None:
        self.component.storage = []
        self.component.refresh_list()

    def collect(self) -> Optional[list[BaseModel]]:
        if len(self.component.storage) == 0 and self.normalized_type.is_nullable:
            return None

        return self.component.storage

    @staticmethod
    def get_record_title(model: BaseModel) -> Optional[str]:
        """
        Пытается получить первый попавшийся атрибут с типом str из модели BaseModel.
        """
        # Перебираем все поля модели
        for field_name, field_info in model.model_fields.items():
            # Получаем значение атрибута
            value = getattr(model, field_name)

            if isinstance(value, str):
                return value

        return None

    def render(self) -> Element:
        self.model_type = extract_inner_type(self.normalized_type.origin_type)

        self.component = ListComponent(
            storage=self.default_value if self.default_value else [],
            record_title_getter=self.get_record_title,
            model=self.model_type,
        )
        el = self.component.render()
        return el

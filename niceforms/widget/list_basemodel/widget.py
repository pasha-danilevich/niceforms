from typing import Optional, Any, Callable

from nicegui.element import Element
from pydantic import BaseModel

from niceforms import BaseWidget
from .component import Column
from ...utils import extract_inner_type


class ListBaseModelWidget(BaseWidget):

    def __init__(
        self, title_getter: Optional[Callable[[BaseModel], str]] = None, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.title_getter = title_getter
        self.kwargs = kwargs
        self._model_type = None
        self._column: Optional[Column[BaseModel]] = None

        self._model_type = extract_inner_type(self.normalized_type.origin_type)

    @property
    def form(self):
        raise Exception(
            f"""{self.__class__.__name__} has more than one form, this property is not available.
            To get the form, use the .component.create_form or .component.records[i].create_form or .component.records[i].create_form attribute."""
        )

    @property
    def column(self) -> Column[BaseModel]:
        assert (
                self._column is not None
        ), 'Component has not been set. Call .render() first.'
        return self._column

    @property
    def model_type(self) -> type[BaseModel]:
        assert self._model_type is not None, 'Model type has not been set.'
        return self._model_type

    def fill(self, data: Optional[list[dict[str, Any] | BaseModel]]) -> None:
        if data is None:
            self.column.storage = []
            return

        result = []
        for item in data:
            if isinstance(item, BaseModel):
                # Если это уже модель, используем её напрямую
                result.append(item)
            else:
                # Если это словарь, создаём модель
                result.append(self.model_type(**item))

        self.column.storage = result
        self.column.refresh_list()

    def validate(self) -> Optional[str]:
        if not self.normalized_type.is_nullable and self.column.storage is None:
            return 'Не должно быть пусто'
        return None

    def clear(self) -> None:
        self.column.storage = []
        self.column.refresh_list()

    def collect(self) -> Optional[list[BaseModel]]:
        if len(self.column.storage) == 0 and self.normalized_type.is_nullable:
            return None

        return self.column.storage

    @staticmethod
    def default_record_title(model: BaseModel) -> Optional[str]:
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

        self._column = Column(
            storage=self.default_value if self.default_value else [],
            record_title_getter=self.title_getter or self.default_record_title,
            kwarg=self.kwargs,
            model_type=self.model_type,
        )
        el = self.column.render()
        return el

    def set_enabled(self, value: bool) -> None:
        self.column.add_button.set_visibility(value)

        for record in self.column.records:
            record.edit_button.set_visibility(value)
            record.delete_button.set_visibility(value)

        self.label.close_button.set_visibility(value)

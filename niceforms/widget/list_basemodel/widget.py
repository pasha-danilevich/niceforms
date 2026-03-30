from typing import Optional, Any, Callable

from nicegui.element import Element
from pydantic import BaseModel

from niceforms import BaseWidget
from ...utils import extract_inner_type
from .component import ListComponent


class ListBaseModelWidget(BaseWidget):

    def __init__(
        self, title_getter: Optional[Callable[[BaseModel], str]] = None, **kwargs: dict
    ) -> None:
        super().__init__(**kwargs)
        self.title_getter = title_getter
        self._model_type = None
        self._component: Optional[ListComponent[BaseModel]] = None

    @property
    def form(self):
        assert (
            self._form is not None
        ), f"Form must be set for {self.__class__.__name__}. Call .render() first."
        return self._form

    @property
    def component(self) -> ListComponent[BaseModel]:
        assert (
            self._component is not None
        ), 'Component has not been set. Call .render() first.'
        return self._component

    @property
    def model_type(self) -> type[BaseModel]:
        if self._model_type is None:
            raise ValueError('Не установлен тип модели')

        return self._model_type

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
        self._model_type = extract_inner_type(self.normalized_type.origin_type)

        from niceforms import BaseModelForm

        self._form = BaseModelForm(
            model=self.model_type,
            title=None,
            view_annotation_type=False,
            view_clear_button=False,
            view_json_button=False,
            view_submit_button=False,
        )

        self._component = ListComponent(
            storage=self.default_value if self.default_value else [],
            record_title_getter=self.title_getter or self.get_record_title,
            form=self._form,
        )
        el = self.component.render()
        return el

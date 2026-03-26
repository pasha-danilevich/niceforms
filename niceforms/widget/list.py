import json
from typing import List, Optional, Union

from nicegui import ui
from nicegui.elements.mixins.validation_element import ValidationElement

from utils import normalize_type
from widget import BaseValidationWidget


class ListWidget(BaseValidationWidget):
    type_tip_map: dict[type, str] = {
        List[str]: '["яблоко", "банан", "апельсин"]',
        List[int]: '[423, 324, 983]',
        list[str]: '["яблоко", "банан", "апельсин"]',
        list[int]: '[423, 324, 983]',
    }

    def collect(self) -> Optional[Union[list, tuple]]:
        if self.element.value is not None:
            try:
                return json.loads(self.element.value)
            except json.decoder.JSONDecodeError:
                return None

        return None

    def render(self) -> ValidationElement:
        default_value = (
            json.dumps(self.default_value) if self.default_value is not None else None
        )

        def decode_validate(v) -> bool:
            try:
                if v:
                    json.loads(v)
            except json.decoder.JSONDecodeError:
                return False

            return True

        validation = {
            **self.default_validations,
            'Не валидный JSON': lambda v: decode_validate(v),
        }

        el = (
            ui.textarea(
                value=default_value,
                placeholder=self.placeholder,
                validation=validation,
            )
            .props("outlined dense")
            .classes("w-full font-mono")
        )
        # Контейнер для лейбла и иконки
        with ui.row().classes('items-center gap-1'):
            ui.label(text=f'Строка парсится как JSON').classes('text-xs mt-1')
            normalized_type = normalize_type(self.field.annotation)

            example = self.type_tip_map.get(normalized_type.origin_type)
            if example is not None:
                # Иконка с подсказкой при наведении
                ui.icon('info', size='xs').classes('cursor-help mt-1').tooltip(
                    f'Пример ввода: {example}'
                ).style('color: #8989ff')

        return el

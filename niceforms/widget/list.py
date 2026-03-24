import json
from datetime import datetime
from json import JSONDecodeError
from typing import Any, List, Optional, Union

from nicegui import ui
from utils import normalize_type

from niceforms.widget import BaseWidget, RenderedWidget


class RenderedListWidget(RenderedWidget):

    def collect(self) -> Optional[Union[list, tuple]]:
        if self.element.value is not None:
            return json.loads(self.element.value)

        return None


class ListWidget(BaseWidget):
    type_tip_map: dict[type, str] = {
        List[str]: '["яблоко", "банан", "апельсин"]',
        List[int]: '[423, 324, 983]',
        list[str]: '["яблоко", "банан", "апельсин"]',
        list[int]: '[423, 324, 983]',
    }

    def render(self) -> RenderedWidget:
        default_value = (
            json.dumps(self.default_value) if self.default_value is not None else None
        )

        el = (
            ui.textarea(value=default_value, placeholder=self.placeholder)
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

        return RenderedListWidget(self, el)

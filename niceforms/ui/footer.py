import logging
from typing import Any, Optional

from actions import OnSubmit
from nicegui import ui
from nicegui.elements.button import Button
from pydantic import BaseModel
from ui.json_viewer import JsonDialog
from widget import BaseWidget

from niceforms import PRIMARY_COLOR_GRADIENT, UIComponent

logger = logging.getLogger(__name__)


class Footer(UIComponent):
    def __init__(
        self,
        widgets: list[BaseWidget],
        model: type[BaseModel],
        on_submit: Optional[OnSubmit],
        view_clear_button: bool = True,
        view_json_button: bool = True,
    ) -> None:
        self.widgets = widgets
        self.model = model
        self.on_submit = on_submit
        self.view_clear_button = view_clear_button
        self.view_json_button = view_json_button

        self._write_to_form_button: Optional[Button] = None
        self._submit_button: Optional[Button] = None

    def init_base_model(self) -> BaseModel:
        data: dict[str, Any] = {}

        for w in self.widgets:
            data[w.field_name] = w.collect()

        return self.model(**data)

    def clear_form(self) -> None:
        logger.debug('Cleared form')
        for w in self.widgets:
            w.clear()

    def render_json_viewer_dialog(self) -> None:
        JsonDialog(model=self.init_base_model()).render()

    def _write_nested_form_to_main_form(self) -> None:
        pass

    async def submit(self) -> None:

        if self.on_submit is None:
            logger.warning(f"on_submit function do not provided")
            return None

        await self.on_submit(self.init_base_model())
        return None

    def render(self) -> None:
        with ui.row().classes("w-full justify-end gap-3"):
            if self.view_clear_button:
                ui.button("Очистить", on_click=self.clear_form).props(
                    "outlined flat"
                ).classes("px-6 py-2")

            if self.view_json_button:
                ui.button(
                    "Показать json", on_click=self.render_json_viewer_dialog
                ).props("outlined flat").classes("px-6 py-2")

            self._submit_button = (
                ui.button("Отправить", on_click=self.submit, icon="send")
                .props("unelevated")
                .classes(f"{PRIMARY_COLOR_GRADIENT} text-white px-8 py-2")
            )

import logging
from typing import Callable, Optional

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.button import Button
from pydantic import BaseModel

from .button import FormButton
from .ui_component import UIComponent
from ..actions import OnSubmit

logger = logging.getLogger(__name__)


class Footer(UIComponent):
    def __init__(
        self,
        model: type[BaseModel],
        on_submit: Optional[OnSubmit],
        on_collect: Callable,
        buttons: list[Callable[[], ui.button]],
    ) -> None:
        self.model = model
        self.on_submit = on_submit
        self.collect = on_collect
        self.buttons = buttons
        self._write_to_form_button: Optional[Button] = None
        self._submit_button: Optional[Button] = None

        self._root: Optional[Element] = None

    @property
    def root(self) -> Element:
        if self._root is None:
            raise ValueError("Not rendered")
        return self._root

    def render(self) -> Element:
        with ui.row().classes("w-full justify-end gap-3") as self._root:
            for button in self.buttons:
                button()

        return self.root

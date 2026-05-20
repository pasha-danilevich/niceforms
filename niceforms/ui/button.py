import abc
from typing import Optional

from nicegui import ui
from nicegui.defaults import DEFAULT_PROP
from nicegui.element import Element
from nicegui.events import Handler, ClickEventArguments

from .ui_component import UIComponent


class FormButton(UIComponent):
    def __init__(
        self,
        text: str,
        on_click: Handler[ClickEventArguments] | None = None,
        icon: Optional[str] = None,
        classes: str = "",
        style: str = "",
        bg_color: str = "gray",
        color_weight: int = 100,
    ) -> None:
        self.text = text
        self.on_click = on_click
        self.icon = icon
        self.extra_classes = classes
        self.style = style
        self.bg_color = bg_color
        self.color_weight = color_weight

    def render(self) -> Element:
        btn = (
            ui.button(self.text)
            .props("flat color=none")
            .classes(
                "rounded-xl "
                f"bg-{self.bg_color}-{self.color_weight} hover:bg-{self.bg_color}-{self.color_weight + 100} "
                f"{self.extra_classes}"
            )
            .style(self.style)
        )
        
        
        
        if self.icon:
            btn.props(f"icon={self.icon}")

        if self.on_click:
            btn.on_click(self.on_click)

        return btn
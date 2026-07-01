from typing import Optional

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.button import Button
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

    def render(self) -> Button:
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

class PositiveButton(FormButton):
    def __init__(
        self,
        text: str,
        on_click: Handler[ClickEventArguments] | None = None,
        icon: Optional[str] = None,
        classes: str = "px-12",
        style: str = 'color: white',
        bg_color: str = "green",
        color_weight: int = 500,
    ) -> None:
        super().__init__(text, on_click, icon, classes, style, bg_color, color_weight)

class NegativeButton(FormButton):
    def __init__(
        self,
        text: str,
        on_click: Handler[ClickEventArguments] | None = None,
        icon: Optional[str] = None,
        classes: str = "px-12",
        style: str = 'color: white',
        bg_color: str = "red",
        color_weight: int = 500,
    ) -> None:
        super().__init__(text, on_click, icon, classes, style, bg_color, color_weight)


class DefaultButton(FormButton):
    def __init__(
        self,
        text: str,
        on_click: Handler[ClickEventArguments] | None = None,
        icon: Optional[str] = None,
        classes: str = "px-8",
        style: str = 'color: gray',
        bg_color: str = "gray",
        color_weight: int = 100,
    ) -> None:
        super().__init__(text, on_click, icon, classes, style, bg_color, color_weight)

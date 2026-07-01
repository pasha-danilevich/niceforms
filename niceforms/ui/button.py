from typing import Optional

from nicegui import ui
from nicegui.elements.button import Button
from nicegui.events import Handler, ClickEventArguments


class FormButton(ui.button):
    def __init__(
        self,
        text: str,
        on_click: Handler[ClickEventArguments] | None = None,
        icon: Optional[str] = None,
        bg_color: str = "gray",
        color_weight: int = 100,
    ) -> None:
        super().__init__(text, on_click=on_click, icon=icon)
        self.text = text
        self.on_click = on_click
        self.icon = icon
        self.bg_color = bg_color
        self.color_weight = color_weight
        
        self.props("flat color=none").classes(
            "rounded-xl "
            f"bg-{self.bg_color}-{self.color_weight} hover:bg-{self.bg_color}-{self.color_weight + 100} "
        )
        
        if self.icon:
            self.props(f"icon={self.icon}")


class PositiveButton(FormButton):
    def __init__(
        self,
        text: str,
        on_click: Handler[ClickEventArguments] | None = None,
        icon: Optional[str] = None,
        bg_color: str = "green",
        color_weight: int = 500,
    ) -> None:
        super().__init__(text, on_click, icon, bg_color, color_weight)
        self.style('color: white')
        self.classes('px-12')


class NegativeButton(FormButton):
    def __init__(
        self,
        text: str,
        on_click: Handler[ClickEventArguments] | None = None,
        icon: Optional[str] = None,
        bg_color: str = "red",
        color_weight: int = 500,
    ) -> None:
        super().__init__(text, on_click, icon, bg_color, color_weight)
        self.style('color: white')
        self.classes('px-12')


class DefaultButton(FormButton):
    def __init__(
        self,
        text: str,
        on_click: Handler[ClickEventArguments] | None = None,
        icon: Optional[str] = None,
        bg_color: str = "gray",
        color_weight: int = 100,
    ) -> None:
        super().__init__(text, on_click, icon, bg_color, color_weight)
        self.style('color: gray')
        self.classes('px-8')

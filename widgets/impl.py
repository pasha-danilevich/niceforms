from nicegui import ui

from widgets.factory import Widget


class StrWidget(Widget):

    def render(self) -> None:
        placeholder = metadata.get(
            "placeholder", self._get_default_placeholder(base_type, label)
        )

        ui.input(placeholder=placeholder).props("outlined dense").classes("w-full")
from nicegui import ui
from widget import BaseWidget


class Body:
    def __init__(self, widgets: list[BaseWidget]) -> None:
        self.widgets = widgets

    def render(self) -> list[BaseWidget]:
        widgets = []

        with ui.column().classes(f"w-full space-y-3 p-1 sm:p-4"):
            for w in self.widgets:
                with ui.element().classes(f"w-full"):
                    w.render_label()
                    el = w.render()
                    w.set_element(el)

                    widgets.append(w)

        return widgets

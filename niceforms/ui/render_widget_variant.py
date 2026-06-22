from typing import cast

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.mixins.validation_element import ValidationElement

from niceforms import BaseWidget, BaseValidationWidget


def default(widget: BaseWidget) -> Element:
    w = widget
    with ui.element().classes(f"w-full") as root:
        w.render_label()
        el = w.render()
        w.set_element(el)

        if not isinstance(w, BaseValidationWidget):
            w.render_error()

        if isinstance(w.element, ValidationElement):
            el = cast(ValidationElement, w.element)
            el.on('blur', el.validate)
    return root

def inline(widget: BaseWidget) -> Element:
    w = widget
    title = w.field.title if w.field.title else w.field_name.title()

    with ui.row().classes("w-full grid grid-cols-12 items-center") as root:

        with ui.row().classes(
            "col-span-3 min-w-0 items-center gap-1 text-grey-8 pb-[20px]"
        ):
            ui.label(title).classes("""
                text-sm
                font-medium
                truncate
                min-w-0
                """).tooltip(title)

            if w.field.description:
                ui.icon(
                    "help_outline",
                    size="12px",
                ).classes(
                    "cursor-help text-grey-5 shrink-0 pb-2"
                ).tooltip(w.field.description)

        with ui.row().classes("col-span-9 justify-end"):
            el = w.render()
            w.set_element(el)

            if isinstance(w.element, ValidationElement):
                el = cast(ValidationElement, w.element)
                el.on('blur', el.validate)

    return root


VARIANTS = {
    'default': default,
    'inline': inline,
}

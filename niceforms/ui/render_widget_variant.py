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

def slim(widget: BaseWidget) -> Element:
    w = widget
    with ui.element().classes(f"w-full") as root:
        title = w.field.title if w.field.title else w.field_name.title()

        with ui.row().classes('w-full items-center'):
            ui.label(title).classes('basis-48')

            el = w.render()
            el.classes('flex-1')
            if w.field.description:
                el.tooltip(w.field.description)

        w.set_element(el)

        if not isinstance(w, BaseValidationWidget):
            w.render_error()

        if isinstance(w.element, ValidationElement):
            el = cast(ValidationElement, w.element)
            el.on('blur', el.validate)
    return root

VARIANTS = {
    'default': default,
    'slim': slim,
}

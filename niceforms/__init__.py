from typing import Type, Optional

from nicegui import ui
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from actions import OnSubmit
from constants import *
from ui import UIComponent
from ui.body import Body
from ui.footer import Footer
from ui.header import Header
from widget_factory import WidgetFactory

factory = WidgetFactory()


class BaseModelForm(UIComponent):
    def __init__(
            self,
            model: Type[BaseModel],
            on_submit: Optional[OnSubmit] = None,
            title: Optional[str] = None,
    ) -> None:
        """Initialize universal form.

        Args:
            model: Pydantic model class
            on_submit: Callback function for form submission
            title: Form title (if None, uses model name)
        """
        self.model = model
        self.on_submit = on_submit
        self.title = title or model.__name__

    def render(self) -> None:
        """Render the form UI."""
        fields: dict[str, FieldInfo] = self.model.model_fields  # type: ignore
        widgets = factory.build(model_fields=fields)

        with ui.card().classes(
                f"w-full {DEFAULT_FORM_WIDTH} mx-auto shadow-lg rounded-xl overflow-hidden"
        ):
            Header(title=self.title, description=self.model.__doc__).render()
            elements = Body(widgets).render()
            Footer(elements=elements, is_nested=False, model=self.model, on_submit=self.on_submit).render()

        # self._render_header(schema)
        # self._render_body(properties)
        # self._render_footer_buttons()

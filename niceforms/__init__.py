import logging
from pprint import pprint
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
from utils import get_nested_models
from widget_factory import WidgetFactory

logger = logging.getLogger(__name__)
factory = WidgetFactory()


class BaseModelForm(UIComponent):
    def __init__(
        self,
        model: Type[BaseModel],
        on_submit: Optional[OnSubmit] = None,
        title: Optional[str] = None,
        header_bg_color: Optional[str] = None,
        view_annotation_type: bool = True,
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
        self.header_bg_color = header_bg_color
        self.view_annotation_type = view_annotation_type

        # style
        self._card = None # тело всей формы
        self._is_nested = False

    def render(self) -> None:
        """Render the form UI."""
        nested_models = get_nested_models(self.model)
        fields: dict[str, FieldInfo] = self.model.model_fields  # type: ignore

        for n_model in nested_models:
            try:
                del fields[n_model.field_name]
            except KeyError:
                logger.debug(f'Field "{n_model.field_name}" is not defined')

        widgets = factory.build(
            model_fields=fields, view_annotation_type=self.view_annotation_type
        )

        with ui.card().classes(
            f"w-full {DEFAULT_FORM_WIDTH} mx-auto shadow-lg rounded-xl overflow-hidden"
        ) as self._card:
            Header(
                title=self.title,
                description=self.model.__doc__,
                bg_color=self.header_bg_color,
                parent_card=self._card,
                is_nested=self._is_nested,
            ).render()

            elements = Body(widgets).render()

            for n_model in nested_models:
                if not self._is_nested:
                    nested_form = BaseModelForm(n_model.model, header_bg_color='#2eeead')
                    nested_form._is_nested = True
                    nested_form.render()
                    nested_form._card.style('height: 100px')

            Footer(
                elements=elements,
                is_nested=self._is_nested,
                model=self.model,
                on_submit=self.on_submit,
            ).render()

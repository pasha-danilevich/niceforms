from typing import Optional, Any

from nicegui.element import Element

from niceforms import BaseWidget


class NestedWidget(BaseWidget):
    BG_COLOR = "#2eeead"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.model = self.normalized_type.origin_type
        self.view_type_error_message = kwargs.get('view_type_error_message', True)
        
        from niceforms import BaseModelForm

        self._form = BaseModelForm(
            model=self.model,
            title=self.field.title if self.field.title else self.field_name.title(),
            # description=n_model.field_info.description,
            header_bg_color=self.BG_COLOR,
            on_submit=None,
            view_annotation_type=self.view_annotation_type,
            view_type_error_message=self.view_type_error_message,
            _is_nullable=self.normalized_type.is_nullable,
        )
        del self._form.buttons['json']
        del self._form.buttons['clear']
        
        self._form._is_nested = True

    def collect(self) -> Optional[Any]:
        if self.form.header.is_none:
            return None

        return self.form.build_model()
    
    def set_enabled(self, value: bool) -> None:
        self.form.set_enabled(value)
        self.form.header.delete_icon.set_visibility(value)
    
    def render(self) -> Element:
        self.form.render_without_wrapper()
        self.form.body.root.set_visibility(False)
        return Element()

    def fill(self, data: Any | None) -> None:
        self.form.fill(data)

    def validate(self) -> Optional[str]:
        pass

    def clear(self) -> None:
        self.form.clear()

    def render_label(self) -> None:
        pass

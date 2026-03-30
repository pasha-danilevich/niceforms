from typing import Optional


class FormError(Exception):
    def __init__(self, form_name: str, message: Optional[str] = None) -> None:
        self.message = message or f"Error in form: {form_name}"

    def __str__(self) -> str:
        return self.message


class FieldNotFound(Exception):
    def __init__(self, field_name: str) -> None:
        self.message = f'Field "{field_name}" not found'

    def __str__(self) -> str:
        return self.message


class CustomizationError(Exception):

    def __str__(self) -> str:
        return 'Customization is not available after rendering. Run .custom_widget() before .render().'

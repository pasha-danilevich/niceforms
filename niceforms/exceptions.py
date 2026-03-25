from typing import Optional


class FormError(Exception):
    def __init__(self,form_name: str, message: Optional[str] = None) -> None:
        self.message = message or f"Error in form: {form_name}"

    def __str__(self) -> str:
        return self.message

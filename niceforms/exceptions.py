from typing import Optional


class FormError(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message or "Error in form"

    def __str__(self) -> str:
        return self.message

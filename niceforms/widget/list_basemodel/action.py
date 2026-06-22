from typing import Protocol

from nicegui.elements.dialog import Dialog
from pydantic import BaseModel


class SaveAction(Protocol):
    def __call__(self, model: BaseModel, dialog: Dialog) -> None: ...


class EditAction(Protocol):
    def __call__(self, model: BaseModel, index: int, dialog: Dialog) -> None: ...

class DeleteAction(Protocol):
    def __call__(self, model: BaseModel, index: int) -> None: ...

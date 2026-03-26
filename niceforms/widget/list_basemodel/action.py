from typing import Protocol

from pydantic import BaseModel


class SaveAction(Protocol):
    def __call__(self, model: BaseModel) -> None: ...


class EditAction(Protocol):
    def __call__(self, model: BaseModel, index: int) -> BaseModel: ...


class DeleteAction(Protocol):
    def __call__(self, model: BaseModel, index: int) -> None: ...

from typing import Protocol

from pydantic import BaseModel

# TODO: сделать T типом
class OnSubmit(Protocol):
    async def __call__(self, model: BaseModel) -> None: ...


class CollectFormData(Protocol):
    def __call__(self) -> BaseModel: ...

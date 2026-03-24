from typing import Protocol

from pydantic import BaseModel


class OnSubmit(Protocol):
    async def __call__(self, model: BaseModel) -> None: ...


class Collect(Protocol):
    def __call__(self) -> BaseModel: ...

from typing import Protocol

from .utils import T


class OnSubmit(Protocol):
    async def __call__(self, model: T) -> None: ...


class BuildModel(Protocol):
    def __call__(self) -> T: ...

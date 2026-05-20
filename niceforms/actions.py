from typing import Callable, Awaitable, TypeAlias

from pydantic import BaseModel

from .utils import T

OnSubmit: TypeAlias = Callable[[T], None | Awaitable[None]]
BuildModel: TypeAlias = Callable[[], BaseModel]

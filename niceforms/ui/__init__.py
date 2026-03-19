"""Компоненты пользовательского интерфейса."""
from abc import ABC, abstractmethod
# from .header import Header
# from .body import Body

class UIComponent(ABC):

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError()




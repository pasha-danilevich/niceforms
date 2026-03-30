"""Компоненты пользовательского интерфейса."""

from abc import ABC, abstractmethod


class UIComponent(ABC):

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError()

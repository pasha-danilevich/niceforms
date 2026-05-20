"""Компоненты пользовательского интерфейса."""

from abc import ABC, abstractmethod

from nicegui.element import Element


class UIComponent(ABC):

    @abstractmethod
    def render(self) -> Element:
        raise NotImplementedError()

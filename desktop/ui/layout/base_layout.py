"""
Gorgon OS (VOS)

Base layout class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from desktop.ui.core.container import Container

class BaseLayout(ABC):
    """
    Base class for all layouts.
    """

    def __init__(self, spacing: int = 0, margin: int = 0) -> None:

        self.spacing = spacing

        self.margin = margin

    @abstractmethod
    def apply(self, container: Container) -> None:
        """
        Arrange the children of the container.
        """
        raise NotImplementedError

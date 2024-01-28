from abc import ABC, abstractmethod
from typing import Optional


class Controller(ABC):
    """Base abstract class of db models controller."""
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

    @abstractmethod
    def list(self, filters: Optional[dict] = None):
        pass

    @abstractmethod
    def get(self, id: int):
        pass

from abc import ABC, abstractmethod
from typing import Optional

class Controller(ABC):
    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

    @abstractmethod
    def list(self, filters: Optional[dict] = None):
        pass

    @abstractmethod
    def get(self):
        pass
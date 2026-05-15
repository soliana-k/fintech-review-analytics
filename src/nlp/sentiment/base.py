from abc import ABC, abstractmethod
from typing import Dict

class SentimentStrategy(ABC):
    @abstractmethod
    def analyze(self, text: str) -> Dict[str, any]:
        pass
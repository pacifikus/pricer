from abc import ABC, abstractmethod
from datetime import date
from QuoteProvider import QuoteProvider


class PriceableElement(ABC):
    @abstractmethod
    def getPrice(self, valuationDate: date, market: QuoteProvider) -> float:
        pass

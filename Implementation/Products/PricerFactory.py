from abc import ABC, abstractmethod
from datetime import date
from typing import List

from Products.QuoteProvider import QuoteProvider
from Products.Pricer import Pricer


class PricerFactory(ABC):
    @abstractmethod
    def createPricer(
        self,
        valuationDate: date,
        underlyings: List[str],
        marker: QuoteProvider
    ) -> Pricer:
        pass

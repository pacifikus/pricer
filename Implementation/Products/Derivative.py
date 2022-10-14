from abc import ABC, abstractmethod
from datetime import date

from PriceableElement import PriceableElement
from Products.Pricer import Pricer
from Products.PricerFactory import PricerFactory
from Products.QuoteProvider import QuoteProvider


class Derivative(PriceableElement, ABC):
    def __init__(self):
        self.pricer = None

    @abstractmethod
    def getPrice(self, valuationDate: date, market: QuoteProvider) -> float:
        pass

    @abstractmethod
    def getBasePrice(self, valuationDate: date, pricer: Pricer) -> float:
        pass

    def setPricerCreator(self, newPricerCreator: PricerFactory):
        self.pricer = newPricerCreator.createPricer()

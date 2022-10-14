from datetime import date

from PriceableElement import PriceableElement
from abc import ABC, abstractmethod

from Products.QuoteProvider import QuoteProvider
from Products.Pricer import Pricer
from Products.PricerFactory import PricerFactory


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

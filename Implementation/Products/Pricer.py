from abc import ABC, abstractmethod
from datetime import date
from Products.CashFlow import CashFlow


class Pricer(ABC):
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def getValuationDate(self) -> date:
        pass

    @abstractmethod
    def getDiscountFactor(self, paymentDate: date) -> date:
        pass

    @abstractmethod
    def getCallOptionBasePrice(
        self, underlying: str, strike: float, maturityDate: date
    ) -> float:
        pass

    @abstractmethod
    def CashFlowBasePrice(self, priceElement: CashFlow) -> float:
        pass


class class_for_test(Pricer):
    def init(self):
        pass

    def getValuationDate(self) -> date:
        pass

    def getDiscountFactor(self, paymentDate: date) -> date:
        pass

    def getCallOptionBasePrice(
        self, underlying: str, strike: float, maturityDate: date
    ) -> float:
        pass

    def CashFlowBasePrice(self, priceElement: CashFlow) -> float:
        pass


r = class_for_test()

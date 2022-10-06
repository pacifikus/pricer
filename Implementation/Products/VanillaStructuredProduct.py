from datetime import date
from typing import List

from Products.Pricer import Pricer
from Products.QuoteProvider import QuoteProvider


class VanillaStructuredProduct:

    def __init__(
        self,
        underlying: str,
        participation: float,
        strike: float,
        maturityDate: date,
        cap: float = None,
        profitZoneStart: float = None,
    ):
        self.__underlying = underlying
        self.__participation = participation
        self.__strike = strike
        self.__maturityDate = maturityDate
        self.__cap = cap
        self.__profitZoneStart = profitZoneStart

    def getPaymentDates(self) -> List[date]:
        return [self.__maturityDate]

    def getPaymentAmount(
        self,
        paymentDate: date,
        market: QuoteProvider,
    ) -> float:
        quotes = market.getQuotes(self.__underlying, [paymentDate])[0]
        profit = max(quotes - self.__strike, 0) / self.__strike
        if self.__cap and profit >= self.__profitZoneStart:
            return 1 + self.__participation * self.__cap
        else:
            return 1 + self.__participation * profit

    def getBasePrice(self, valuationDate: date, pricer: Pricer) -> float:
        pass

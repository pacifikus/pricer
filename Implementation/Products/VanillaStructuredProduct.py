from datetime import date
from typing import List

from Products.QuoteProvider import QuoteProvider


class VanillaStructuredProduct:

    def __init__(
        self,
        underlying: str,
        participation: float,
        strike: float,
        maturityDate: date
    ):
        self.__underlying = underlying
        self.__participation = participation
        self.__strike = strike
        self.__maturityDate = maturityDate

    def getPaymentDates(self) -> List[date]:
        return [self.__maturityDate]

    def getPaymentAmount(
        self,
        paymentDate: date,
        market: QuoteProvider
    ) -> float:
        return \
            1 \
            + self.__participation * max(
                market.getQuotes(self.__underlying, [paymentDate])[0]
                - self.__strike,
                0
            ) / self.__strike

    # def getBasePrice(self, valuationDate: date, pricer: Pricer) -> float:
    #     pass

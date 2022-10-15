from datetime import date
from math import log
from typing import List

from Products.CashFlow import CashFlow
from Products.Pricer import Pricer
from Products.QuoteProvider import QuoteProvider
from scipy.stats import norm
from Simulation.CovarianceTermStructure import CovarianceTermStructure
from Simulation.DiscountCurve import DiscountCurve


class SimulationPricer(Pricer):
    def __init__(
        self,
        underlyings: List[str],
        valuationDate: date,
        originalMarket: QuoteProvider,
        discountCurve: DiscountCurve,
        covariance: CovarianceTermStructure,
    ):
        self.__underlyings = underlyings
        self.__valuationDate = valuationDate
        self.__originalMarket = originalMarket
        self.__discountCurve = discountCurve
        self.__covariance = covariance

    def getDiscountFactor(self, paymentDate: date) -> float:
        return self.__discountCurve.getDiscountFactor(paymentDate)

    def getCallOptionBasePrice(
        self, underlying: str, strike: float, maturityDate: date
    ) -> float:
        totalVariance = self.__covariance.getTotalCovariance(maturityDate)
        spotPrice = self.__originalMarket.getQuotes(
            ticker=underlying, observationDates=[self.__valuationDate]
        )[0]
        discountFactor = self.getDiscountFactor(self.__valuationDate)
        forwardPrice = spotPrice / discountFactor
        d_1 = log(
            (forwardPrice / strike) + (totalVariance ** 2) / 2
        ) / totalVariance
        d_2 = d_1 - totalVariance
        N_1 = norm.cdf(d_1)
        N_2 = norm.cdf(d_2)
        return discountFactor * (forwardPrice * N_1 - strike * N_2)

    def getCashFlowBasePrice(self, pricedElement: CashFlow) -> float:
        pass

    def getValuationDate(self) -> date:
        return self.__valuationDate

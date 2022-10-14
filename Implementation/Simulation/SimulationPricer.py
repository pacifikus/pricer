from datetime import date
from typing import List

from math import log
from scipy.stats import norm

from Products.CashFlow import CashFlow
from Products.Pricer import Pricer
from Products.QuoteProvider import QuoteProvider
from Simulation.CovarianceTermStructure import CovarianceTermStructure
from Simulation.DiscountCurve import DiscountCurve


class SimulationPricer(Pricer):
    def __init__(
        self,
        underlyings: List[str],
        valuationDate: date,
        originalMarket: QuoteProvider,
        drift: DiscountCurve,
        covariance: CovarianceTermStructure
    ):
        self.__underlyings = underlyings
        self.__valuationDate = valuationDate
        self.__originalMarket = originalMarket
        self.__drift = drift
        self.__covariance = covariance

    def getDiscountFactor(self, paymentDate: date) -> float:
        return self.__drift.getDiscountFactor(paymentDate)

    def getCallOptionBasePrice(
        self,
        underlying: str,
        strike: float,
        maturityDate: date
    ) -> float:
        sigma_T = self.__covariance.getTotalCovariance(maturityDate)
        S_t = self.__originalMarket.getQuotes(
            ticker=underlying,
            observationDates=[self.__valuationDate]
        )[0]
        B_t = self.getDiscountFactor(self.__valuationDate)
        F_t = S_t / B_t
        K = strike
        d_1 = log((F_t / K) + (sigma_T ** 2) / 2) / sigma_T
        d_2 = d_1 - sigma_T
        N_1 = norm.cdf(d_1)
        N_2 = norm.cdf(d_2)
        return B_t * (F_t * N_1 - K * N_2)

    def getCashFlowBasePrice(self, pricedElement: CashFlow) -> float:
        pass

    def getValuationDate(self) -> date:
        return self.__drift.getValuationDate()

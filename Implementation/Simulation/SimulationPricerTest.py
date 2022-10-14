from datetime import date
from math import exp
from typing import List
from unittest import TestCase

from Products.QuoteProvider import QuoteProvider
from Simulation.CovarianceTermStructure import CovarianceTermStructure
from Simulation.DiscountCurve import DiscountCurve
from Simulation.SimulationPricer import SimulationPricer


class CovarianceTermStructureStub(CovarianceTermStructure):
    def getObservationDate(self) -> date:
        pass

    def getTotalCovariance(self, ForecastDate: date):
        return 0.1


class QuoteProviderStub(QuoteProvider):
    def __init__(self, value: float):
        self.__value = value

    def getQuotes(self, ticker: str, observationDates: List[date]) -> List[float]:

        if ticker == "GAZP" and observationDates == [date(2022, 9, 1)]:
            return [self.__value]
        else:
            raise NotImplementedError()


class DiscountCurveStub(DiscountCurve):
    def getValuationDate(self) -> date:
        return date(2022, 9, 1)

    def getDiscountFactor(self, paymentDate) -> float:
        rate = 0.1
        if paymentDate == date(2022, 9, 1):
            return exp(-rate * 30 / 365)
        else:
            raise NotImplementedError()


class SimulationPricerTest(TestCase):
    def setUp(self) -> None:
        self.__testedPricer = SimulationPricer(
            underlyings=["GAZP"],
            covariance=CovarianceTermStructureStub(),
            valuationDate=date(2022, 9, 1),
            originalMarket=QuoteProviderStub(250),
            discountCurve=DiscountCurveStub(),
        )

    def testValuationDate(self):
        self.assertEqual(
            self.__testedPricer.getValuationDate(),
            date(2022, 9, 1),
        )

    def testDiscountFactor(self):
        rate = 0.1
        date_ = date(2022, 9, 1)
        self.assertEqual(
            self.__testedPricer.getDiscountFactor(date_), exp(-rate * 30 / 365)
        )

    def testCallOptionBasePriceInTheMoneyPayoff(self):
        result = self.__testedPricer.getCallOptionBasePrice(
            underlying="GAZP",
            strike=200,
            maturityDate=date(2022, 10, 1),
        )
        expected = 51.71
        self.assertEqual(result, expected)

    def testCallOptionBasePriceOutOfTheMoneyPayoff(self):
        result = self.__testedPricer.getCallOptionBasePrice(
            underlying="GAZP",
            strike=300,
            maturityDate=date(2022, 10, 1),
        )
        expected = 0.45
        self.assertEqual(expected, result)

    def testCallOptionBasePriceAtTheMoneyPayoff(self):
        result = self.__testedPricer.getCallOptionBasePrice(
            underlying="GAZP",
            strike=250,
            maturityDate=date(2022, 10, 1),
        )
        expected = 10.96
        self.assertEqual(expected, result)

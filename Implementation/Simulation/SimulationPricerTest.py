from collections import namedtuple
from datetime import date
from math import exp
from typing import List
from unittest import TestCase
from unittest.mock import patch

import numpy as np
from Products.QuoteProvider import QuoteProvider
from Simulation.SimulationPricer import SimulationPricer


class QuoteProviderStub(QuoteProvider):
    def __init__(self, value: float):
        self.__value = value

    def getQuotes(
        self,
        ticker: str,
        observationDates: List[date]
    ) -> List[float]:

        if ticker == "GAZP" and observationDates == [date(2022, 9, 1)]:
            return [self.__value]
        else:
            raise NotImplementedError()


class SimulationPricerTest(TestCase):
    @patch('Simulation.CovarianceTermStructure')
    @patch('Simulation.DiscountCurve')
    def setUp(self, mockCovarianceTermStructure, mockDiscountCurve) -> None:
        mockCovarianceTermStructure = mockCovarianceTermStructure
        mockCovarianceTermStructure.getTotalCovariance.return_value = \
            np.array([0.01])
        rate = 0.1
        self.__mockDiscountCurve = mockDiscountCurve
        self.__mockDiscountCurve.getDiscountFactor.return_value = exp(
            -rate * 30 / 365
        )

        self.__testedPricer = SimulationPricer(
            underlyings=["GAZP"],
            covariance=mockCovarianceTermStructure,
            valuationDate=date(2022, 9, 1),
            originalMarket=QuoteProviderStub(250),
            discountCurve=mockDiscountCurve,
        )

    def testValuationDate(self):
        self.assertEqual(
            self.__testedPricer.getValuationDate(),
            date(2022, 9, 1),
        )

    def testDiscountFactor(self):
        date_ = date(2022, 9, 1)
        self.assertEqual(
            self.__testedPricer.getDiscountFactor(date_),
            self.__mockDiscountCurve.getDiscountFactor(date_)
        )

    def testCallOptionBasePrice(self):
        TestConfig = namedtuple("TestConfig", "strike expected")
        testMap = {
            'InTheMoney': TestConfig(strike=200, expected=51.71),
            'AtTheMoney': TestConfig(strike=250, expected=10.96),
            'OutOfTheMoney': TestConfig(strike=300, expected=0.45),
        }
        for testCase, testConfig in testMap.items():
            with self.subTest(name=testCase):
                result = self.__testedPricer.getCallOptionBasePrice(
                    underlying="GAZP",
                    strike=testConfig.strike,
                    maturityDate=date(2022, 10, 1),
                )
                self.assertAlmostEqual(result, testConfig.expected, places=1)

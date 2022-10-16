from collections import namedtuple
from datetime import date
from typing import List
from unittest import TestCase

from Products.QuoteProvider import QuoteProvider
from Products.VanillaStructuredProduct import VanillaStructuredProduct


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


class VanillaStructuredProductTest(TestCase):
    def setUp(self) -> None:
        self.__testedUncappedProduct = VanillaStructuredProduct(
            underlying="GAZP",
            participation=0.65,
            strike=250,
            maturityDate=date(2022, 9, 1),
        )
        self.__testedCappedProduct = VanillaStructuredProduct(
            underlying="GAZP",
            participation=0.5,
            strike=250,
            maturityDate=date(2022, 9, 1),
            cap=0.08,
        )

    def testPaymentDates(self):
        self.assertEqual(
            [date(2022, 9, 1)],
            self.__testedUncappedProduct.getPaymentDates()
        )

    def testUncappedPayoff(self):
        testParameters = namedtuple(
            "testParameters",
            "underlyingQuote expected"
        )
        testMap = {
            'In the money': testParameters(
                underlyingQuote=260,
                expected=1 + 0.65 * 10 / 250
            ),
            'At the money': testParameters(underlyingQuote=250, expected=1),
            'Out of the money': testParameters(underlyingQuote=230, expected=1)
        }
        for testCase, testParams in testMap.items():
            with self.subTest(testCase):
                self.assertEqual(
                    testParams.expected,
                    self.__testedUncappedProduct.getPaymentAmount(
                        date(2022, 9, 1),
                        QuoteProviderStub(testParams.underlyingQuote)
                    ),
                )

    def testCappedPayoff(self):
        testParameters = namedtuple(
            "testParameters",
            "underlyingQuote expected"
        )
        testMap = {
            'At the money, with cap': testParameters(
                underlyingQuote=250,
                expected=1
            ),
            'Out of the money, with cap': testParameters(
                underlyingQuote=230,
                expected=1
            ),
            'In the money, strike price': testParameters(
                underlyingQuote=290,
                expected=1 + 0.08
            ),
            'In the money, with cap capped': testParameters(
                underlyingQuote=300,
                expected=1 + 0.08
            ),
            'In the money, with cap non capped': testParameters(
                underlyingQuote=260,
                expected=1 + 0.5 * 10 / 250
            )
        }

        for testCase, testParams in testMap.items():
            with self.subTest(testCase):
                self.assertEqual(
                    testParams.expected,
                    self.__testedCappedProduct.getPaymentAmount(
                        date(2022, 9, 1),
                        QuoteProviderStub(testParams.underlyingQuote)
                    ),
                )

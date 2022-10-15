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
        self.__testedСappedProduct = VanillaStructuredProduct(
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
        for underlyingQuote, expectedResult, testCase in [
            (260, 1 + 0.65 * 10 / 250, "In the money"),
            (250, 1, "At the money"),
            (230, 1, "Out of the money"),
        ]:
            with self.subTest(testCase):
                self.assertEqual(
                    expectedResult,
                    self.__testedUncappedProduct.getPaymentAmount(
                        date(2022, 9, 1),
                        QuoteProviderStub(underlyingQuote)
                    ),
                )
        
    def testCappedPayoff(self):
        for underlyingQuote, expectedResult, testCase in [
            (250, 1, "At the money, with cap"),
            (230, 1, "Out of the money, with cap"),
            (290, 1 + 0.5 * 0.08, "In the money, strike price"),
            (300, 1 + 0.5 * 0.08, "In the money, with cap capped"),
            (260, 1 + 0.5 * 10 / 250, "In the money, with cap non capped"),
        ]:
            with self.subTest(testCase):
                self.assertEqual(
                    expectedResult,
                    self.__testedСappedProduct.getPaymentAmount(
                        date(2022, 9, 1),
                        QuoteProviderStub(underlyingQuote)
                    ),
                )
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
    def testUncappedPayoff(self):
        with self.subTest('Failed: setUp'):
            # Testing seUp of UncappedProduct
            self.__testedUncappedProduct = VanillaStructuredProduct(
                underlying="GAZP",
                participation=0.65,
                strike=250,
                maturityDate=date(2022, 9, 1),
            )

        with self.subTest('Failed: testPaymentDates'):
            # Testing testPaymentDates
            self.assertEqual(
                [date(2022, 9, 1)],
                self.__testedUncappedProduct.getPaymentDates()
            )

        for underlyingQuote, expectedResult, test_case in [
            (260, 1 + 0.65 * 10 / 250, "testInTheMoneyPayoff"),
            (250, 1, "testAtTheMoneyPayoff"),
            (230, 1, "testOutOfTheMoneyPayoff"),
        ]:
            with self.subTest('Failed:', test_case):
                # Testing testInTheMoneyPayoff
                self.assertEqual(
                    expectedResult,
                    self.__testedUncappedProduct.getPaymentAmount(
                        date(2022, 9, 1),
                        QuoteProviderStub(underlyingQuote)
                    ),
                )
        
    def testCappedPayoff(self):
        with self.subTest('Failed: setUp'):
            # Testing setUp of СappedProduct
            self.__testedСappedProduct = VanillaStructuredProduct(
                underlying="GAZP",
                participation=0.5,
                strike=250,
                maturityDate=date(2022, 9, 1),
                cap=0.08,
            )

        for underlyingQuote, expectedResult, test_case in [
            (250, 1, "testAtTheMoneyPayoffWithCap"),
            (230, 1, "testOutOfTheMoneyPayoffWithCap"),
            (290, 1 + 0.5 * 0.08, "testInTheMoneyPayoffWithCapCappedStrikePrice"),
            (300, 1 + 0.5 * 0.08, "testInTheMoneyPayoffWithCapCapped"),
            (260, 1 + 0.5 * 10 / 250, "testInTheMoneyPayoffWithCapNonCapped")
        ]:
            with self.subTest('Failed:', test_case):
                self.assertEqual(
                    expectedResult,
                    self.__testedСappedProduct.getPaymentAmount(
                        date(2022, 9, 1),
                        QuoteProviderStub(underlyingQuote)
                    ),
                )
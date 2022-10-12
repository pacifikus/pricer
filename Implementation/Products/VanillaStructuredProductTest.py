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
        sampleMarket260 = QuoteProviderStub(260)
        sampleMarket250 = QuoteProviderStub(250)
        sampleMarket230 = QuoteProviderStub(230)

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
            
        with self.subTest('Failed: testInTheMoneyPayoff'):
            # Testing testInTheMoneyPayoff
            self.assertEqual(
                1 + 0.65 * 10 / 250,
                self.__testedUncappedProduct.getPaymentAmount(
                    date(2022, 9, 1),
                    sampleMarket260
                ),
            )

        with self.subTest('Failed: testAtTheMoneyPayoff'):
            # Testing testAtTheMoneyPayoff
            self.assertEqual(
                1,
                self.__testedUncappedProduct.getPaymentAmount(
                    date(2022, 9, 1),
                    sampleMarket250
                ),
            )

        with self.subTest('Failed: testOutOfTheMoneyPayoff'):
            # Testing testOutOfTheMoneyPayoff
            self.assertEqual(
                1,
                self.__testedUncappedProduct.getPaymentAmount(
                    date(2022, 9, 1),
                    sampleMarket230
                ),
            )
        
    def testCappedPayoff(self):
        sampleMarket250 = QuoteProviderStub(250)
        sampleMarket230 = QuoteProviderStub(230)
        sampleMarket290 = QuoteProviderStub(290)
        sampleMarket300 = QuoteProviderStub(300)
        sampleMarket260 = QuoteProviderStub(260)

        with self.subTest('Failed: setUp'):
            # Testing setUp of СappedProduct
            self.__testedСappedProduct = VanillaStructuredProduct(
                underlying="GAZP",
                participation=0.5,
                strike=250,
                maturityDate=date(2022, 9, 1),
                cap=0.08,
            )

        with self.subTest('At the money payoff'):
            # At the money payoff with cap
            self.assertEqual(
                1,
                self.__testedСappedProduct.getPaymentAmount(
                    date(2022, 9, 1),
                    sampleMarket250
                ),
            )
        
        with self.subTest('Out of the money payoff'):
            # Out of the money payoff with cap
            self.assertEqual(
                1,
                self.__testedСappedProduct.getPaymentAmount(
                    date(2022, 9, 1),
                    sampleMarket230
                ),
            )

        with self.subTest('In the money payoff'):
            # In the money payoff with cap capped strike price
            self.assertEqual(
                1 + 0.5 * 0.08,
                self.__testedСappedProduct.getPaymentAmount(
                    date(2022, 9, 1),
                    sampleMarket290
                ),
            )
            # In the money payoff with cap capped
            self.assertEqual(
                1 + 0.5 * 0.08,
                self.__testedСappedProduct.getPaymentAmount(
                    date(2022, 9, 1),
                    sampleMarket300
                ),
            )
            # In the money payoff with cap non capped
            self.assertEqual(
                1 + 0.5 * 10 / 250,
                self.__testedСappedProduct.getPaymentAmount(
                    date(2022, 9, 1),
                    sampleMarket260
                ),
            )
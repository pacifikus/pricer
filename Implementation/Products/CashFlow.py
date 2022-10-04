from datetime import date
from datetime import date
from typing import List
from abc import ABC, abstractmethod
import pandas

class CashFlow(ABC):
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def getPaymentDates(self) -> List[date]:
        pass
    
    @abstractmethod
    def getPaymentAmount(
        self,
        paymentDate: [date],
        market: QuoteProvider
        ) -> float:
        pass

class test_cash_flow_class(CashFlow):
    def init(self):
        pass

    def getPaymentDates(self, Product) -> List[date]:
        self.Product = Product
        return self.Product.getPaymentDates()

    def getPaymentAmount(
        self,
        Product,
        paymentDate: [date],
        market: QuoteProvider
        ) -> float:
        self.Product = Product
        return self.Product.getPaymentAmount(self.getPaymentDates(Product), market)
    
    def getCashflow(
        self,
        Product,
        currentDate: [date],
        paymentDate: [date],
        market: QuoteProvider
        ) -> pandas.Series:
        self.Product = Product
        flows = pandas.Series(self.getPaymentAmount(
            Product,
            self.getPaymentDates(Product),
            market), 
            index=self.getPaymentDates(Product), 
            dtype=float)
        print(flows.index, currentDate)
        return flows[flows.index <= currentDate]

Flow = test_cash_flow_class()

from datetime import date
from typing import List
import pandas

class CashFlow:
    def __init__(
        self,
        Product: str #Product - VanillaStructuredProduct or Autocall
    ):
        self.Product = Product


    def getPaymentDates(self) -> List[date]:
        return self.Product.getPaymentDates()

    def getPaymentAmount(
        self,
        paymentDate: [date],
        market: QuoteProvider
        ) -> float:
        return self.Product.getPaymentAmount(self.getPaymentDates(), market)
    
    def getCashflow(
        self,
        currentDate: [date],
        paymentDate: [date],
        market: QuoteProvider
        ) -> pandas.Series:
        
        flows = pandas.Series(self.getPaymentAmount(
            self.getPaymentDates(),
            market), 
            index=[self.getPaymentDates()], 
            dtype=float)
        return flows[flows.index <= currentDate]
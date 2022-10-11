from datetime import date
from typing import List
from Products.QuoteProvider import QuoteProvider

class Autocall:
    def __init__(
        self,
        underlyingAssets: List[str],
        AB: float,
        CB: float,
        startDate: date,
        maturityDate: date,
        observationsAmount: int,
        annulizedCouponLevel: float,
        memoryFeature: bool
    ):
        self.__couponDates = []
        for i in range(observationsAmount):
            self.__couponDates.append(datetime.fromtimestamp(startDate.timestamp() + i * (maturityDate.timestamp() - startDate.timestamp()) / (observationsFrequency - 1)))
        self.__underlyingAssets = underlyingAssets
        self.__annulizedCouponLevel = annulizedCouponLevel
        self.__AB = AB
        self.__CB = CB
        self.__memoryFeature = memoryFeature

    

    def getPaymentDates(self) -> List[date]:
        return self.__couponDates
    

    def findDateIndex(self, date: date) -> int:
        index = -1
        for i in range(len(self.times)):
            if date == self.__couponDates[i]:
                index = i
        return index
    
    def findMinInUnderlyings(self, quotes: List[float]) -> float:
        return min(quotes)
    
    def findMaxInUnderlyings(self, quotes: List[float]) -> float:
        return max(quotes)
    
    def findGlobalMax(self, quotes: List[List[float]]) -> float:
        max = quotes[0][0]
        for i in range(len(quotes)):
            for j in range(len(quotes[i])):
                if max < quotes[i][j]:
                    max = quotes[i][j]
        return max
    
  
    def coupon(self, paymentDate: date, market:QuoteProvider) -> float:
        index = self.findDateIndex(paymentDate)
        underlyingQuotes = [[market.getQuotes(x, self.__couponDates[y]) / market.getQuotes(x, self.__couponDates[0]) for x in self.__underlyingAssets] for y in range(index+1)]
        
        currentMin = min(underlyingQuotes[i])
        mins = [min(underlyingQuotes[j]) for j in range(i)]
        tempMax = max(mins)

        if currentMin >= self.__CB and currentMin < self.__AB and tempMax < self.__AB:
            return self.__annulizedCouponLevel
        else:
            return 0


    def redemption(self, paymentDate: date, market:QuoteProvider) -> float:
        i = self.findDateIndex(paymentDate)
        underlyingQuotes = [[market.getQuotes(x, self.__couponDates[y]) / market.getQuotes(x, self.__couponDates[0]) for x in self.__underlyingAssets] for y in range(index+1)]
        
        currentMin = min(underlyingQuotes[i])
        mins = [min(underlyingQuotes[j]) for j in range(i)]
        tempMax = max(mins)

        if currentMin >= self.__AB and tempMax < self.__AB:
            return 1
        else:
            return 0


    def getPaymentAmount(self, paymentDate: date, market:QuoteProvider) -> float:
        return (self.redemption(paymentDate, market) + self.coupon(paymentDate, market))

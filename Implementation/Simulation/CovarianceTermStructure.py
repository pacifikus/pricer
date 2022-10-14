from datetime import date
from abc import ABC, abstractmethod


class CovarianceTermStructure(ABC):
    @abstractmethod
    def getObservationDate(self) -> date:
        pass

    @abstractmethod
    def getTotalCovariance(self, ForecastDate: date):
        pass

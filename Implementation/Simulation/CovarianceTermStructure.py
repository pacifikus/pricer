from abc import ABC, abstractmethod
from datetime import date


class CovarianceTermStructure(ABC):
    @abstractmethod
    def getObservationDate(self) -> date:
        pass

    @abstractmethod
    def getTotalCovariance(self, ForecastDate: date):
        pass

### Modules

* In the usual case, keep each class in a separate module with the same name.
  E.g., ``RiskFactor`` class must be exclusevly in ``RiskFactor.py`` module.

### Testing

* Write a unit test for each non-trivial class method.
* Use ``unittest`` library.
* Use one unit test class for each class under test.
* Name a test class by adding 'Test' to the class under test name (e.g.,
  ``RiskFactorTest`` for ``RiskFactor`` class).
* Place stub classes for a test in the same module before the test class.

### Typing

* Specify parameter and return types explicitly:
    ```
    # Correct:
    def getFactorValue(self, scopeAssignment: VariableAssignment) -> float:
        pass
    ```
    ```
    # Wrong:
    def getFactorValue(self, scopeAssignment):
        pass
    ```

* Where applicable, use ``typing`` library:
  ```
  from typing import Set, Union
  
  def getVariableSupport(scopeVariable: Union[Variable, str]) -> Set[float]:
      pass
  ```

### Code style

##### General guidelines

Follow PEP8 when it does not contradict the guidelines below.

##### Case

* Use CamelCase for class, type, package, and module names:
  ```
  # Correct:
  from typing import TypeVar
  
  from GrapicalModels.Factor import Factor 
  
  ValueType = TypeVar('ValueType')
  
  
  class DiscreteFactor(Factor):
      pass
  ```

* Use lowerCamelCase for function, method, parameter, member and variable
  names:
  ```
  # Correct: 
  def getNormalizedValue(self, scopeVariable: str) -> float:
     assignedValue = self.__values[scopeVariable]
     return assignedValue / self.__total
  ```    

* For imported names, snake_case is admissible.

###### Rationale

Camel case is very common in UML. Use of different cases in design
and implementation files would be expensive and error-prone. Implementation can
be done in different languages, while design is practically not.

##### Line wrapping

* Limit all lines to a maximum of 79 characters (PEP8).

* If a declaration or call cannot fit into one line,
  place each parameter on a separate line:
  ```
  # Correct:
  def addVariableConditionalDistribution(
      self, 
      variableName: str, 
      newConditionalDistribution: Factor
  ):
      pass
  ```
  ```
  # Correct:
  newFactor = factorCreator.createCustomDiscreteFactor(
      ["C", "A"],
      numpy.array([[0, 0, 0.2]])
  )   
  ```
  ```    
  # Wrong:
  def addVariableConditionalDistribution(
      self, variableName: str, 
      newConditionalDistribution: Factor
  ):
      pass
  ```
  ```
  # Wrong:
  newFactor = factorCreator.createCustomDiscreteFactor(
      ["C", "A"], numpy.array([[0, 0, 0.2]])
  )
  ```

* If an import statement cannot fit into one line,
  wrap it as follows:
  ```
  # Correct:
  from Graphs.DirectedEdgeNodeIteratorWrapper import \
      DirectedEdgeNodeIteratorWrapper
  ```

##### Indentation

* In multiline declarations and calls, use hanging indent with one indentation
  level for parameters:
  ```
  # Correct:
  def getConditionalDistribution(
      self,
      conditioning: VariableAssignment,
      independenceMap: DirectedGraph,
      observationDate: date
  ):
      result = self.__jointDistribution.getReducedFactor(
          conditioning, 
          independenceMap,
          observationDate
      )
  ```
  ```
  # Wrong:
  def getConditionalDistribution(
          self,
          conditioning: VariableAssignment,
          independenceMap: DirectedGraph,
          observationDate: date
  ):
      result = self.__jointDistribution.getReducedFactor(
              conditioning, 
              independenceMap,
              observationDate
      )
  ```

* Line up closing brace/bracket/parenthesis under the first character
  of a multiline construct:
  ```
  # Correct:
  result = self.__jointDistribution.getReducedFactor(
      conditioning, 
      independenceMap,
      observationDate
  )
  ```
  ```
  # Wrong:
  result = self.__jointDistribution.getReducedFactor(
      conditioning, 
      independenceMap,
      observationDate
      )
  ```

##### Naming

* Names should make code to be readable like natural language:
  ```
  # Correct:
  for scopeElement in distributionFactor.getScope():
     pass
  ```
  ```
  # Wrong:
  for var in df.getVars():
     pass
  ```

* Avoid use of abbreviations:
  ```
  # Correct:
  class DynamicBaysianNetwork(ProbabilisticGraphicalModel):
      pass
  ```
  ```
  # Wrong:
  class DBN(PGM):
      pass
  ```

* In most cases variable and parameter names must capture their roles,
  not types:
  ```
  # Correct:
  def addScopeElement(newScopeElement: Variable):
      pass
  ```
  ```
  # Usually wrong:
  def addScopeElement(variable: Variable):
      pass
  ```

##### Imports

* Group imports according to PEP8.

* Sort imports case-sensitively.
* Sort plain and "from" imports separately.
* Sort names in "from" imports.

  ```
  # Correct:
  import copy
  import zipapp
  from typing import Callable, List
  from unittest import TestCase
  
  import QuantLib
  import pandas
  
  from Notification.Observer import Observer
  ```
  ```
  # Wrong:
  import copy
  from unittest import TestCase
  from typing import Callable, List
  import zipapp
  
  import pandas
  import QuantLib
  
  from Notification.Observer import Observer
  ```

  ###### Rationale
  Ordered imports are easier to read and edit.


* Erase unused imports.

* Avoid renaming and abbreviation:
  ```
  # Correct: 
  import pandas
  ```
  ```
  # Wrong:
  import pandas as pd
  ```
  ###### Rationale
  Do not burden a reader by the context knowledge. E.g.,
  'pd' might stand for 'pandas' or 'probability of default'
  in different contexts.

##### Documentation

* Docstrings are not mandatory, with well naming they can be often omitted.
  ```
  # Possible:
  def getSpotExchangeRate(
      self,
      foreignCurrency, str, 
      domesticCurrency: str,
      observationDate: date
  ) -> float:
      pass
  ```
  ```
  # Wrong:
  def getRate(self, fc: str, dc: str, dt: date):
      """
      :param fc: foreign currency code
      :param dc: domestic currency code
      :return: spot fcdc exchange rate
      """
  ```

* Add only valuable docstrings. E.g., the docstrings below add nothing
  to the method signature, therefore they must be omitted or replaced:
  ```
  # Wrong:
  def getModelPrice(self, pricingDate: date, pricingCurrency: str) -> float:
      """
      :param pricingDate: date to calculate price on
      :param pricingCurrency: returned price currency
      :return: instrument price calclulated with model
      """

      pass
  ```

# Python Test Framework

This is a small Python unit testing framework

## Features

- [x] True
- [x] False
- [x] Equal
- [x] NotEqual

## Example Usage

Passing Tests:

```python
from testing import TestCase, Setup, Test, run

my_tests = []

@TestCase(my_tests)
class AdditionTests:
    @Setup
    def _setup(self):
        self.num_1 = 1
        self.num_2 = 2
    
    @Test
    def oneAddTwoIsThree(self):
        result = self.num_1 + self.num_2
        return self.expectEqual(result, 3)
    
    @Test
    def oneAddTwoIsNotFour(self):
        result = self.num_1 + self.num_2
        return self.expectNotEqual(result, 4)

run(my_tests)
```

Output:

```txt
Starting Tests...
Tests Finished.
Tests took: 0:00:00
```

Failing Tests:

```python
from testing import TestCase, Setup, Test, Teardown, run

my_tests = []

@TestCase(my_tests)
class BooleanTests:
    @Test
    def falseAndTrueIsFalse(self):
        result = False and True
        return self.expectTrue(result)

    @Test
    def trueOrTrueIsFalse(self):
        result = True or True
        return self.expectFalse(result)

run(my_tests)
```

Output:

```txt
Starting Tests...
BooleanTests Failing:
        falseAndTrueIsFalse
        trueOrTrueIsFalse
Tests Finished.
Tests took: 0:00:00.000995
```

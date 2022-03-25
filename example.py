import typing as t
from testing import TestCase, Case, Test, Setup, Teardown, run

tests: t.List[TestCase] = []

@Case(tests)
class PassingTests(TestCase):
    @Setup
    def setup(self) -> None:
        self.a = 1
        self.b = 2
    
    @Test
    def passing1(self) -> bool:
        self.b -= 1
        return self.assertEqual(self.a, self.b)

    @Test
    def passing2(self) -> bool:
        return self.assertNotEqual(self.a, self.b)

    @Teardown
    def teardown(self) -> None:
        self.a = 5
        self.b = 8

@Case(tests)
class FailingTests(TestCase):
    @Setup
    def setup(self) -> None:
        self.a = 1
        self.b = 1
    
    @Test
    def failing1(self) -> bool:
        return self.assertNotEqual(self.a, self.b)
    
    @Test
    def failing2(self) -> bool:
        return self.assertTrue(self.a != self.b)

run(tests)
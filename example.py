from testing import Teardown, TestCase, Test, Setup, run

my_tests = []

@TestCase(my_tests)
class FirstSet:
    @Setup
    def _setup(self):
        self.a = 'a'
        self.b = 'b'

    @Test
    def passing(self):
        return self.expectTrue(self.a != self.b)
    
    @Test
    def passing2(self):
        return self.expectFalse(self.a == self.b)
    
    @Teardown
    def _teardown(self):
        self.a = None
        self.b = None

@TestCase(my_tests)
class SecondSet:
    @Test
    def failing(self):
        return self.expectEqual(1+1, 3)
    
    @Test
    def failing2(self):
        return self.expectNotEqual(1+2, 3)

run(my_tests)
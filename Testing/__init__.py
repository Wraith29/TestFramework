from datetime import datetime
from functools import wraps
import typing as t

T = t.TypeVar("T")

def firstOrNone(arr: t.List[T]) -> t.Optional[T]:
    return arr[0] if len(arr) != 0 else None

def getAllInstances(cls: T, name: str) -> t.List[t.Any]:
    return [
        getattr(cls, attr)
        for attr in dir(cls)
        if hasattr(getattr(cls, attr), name)
        and callable(getattr(cls, attr))
    ]

def getFirstInstance(cls: T, name: str) -> t.Optional[t.Callable[[], None]]:
    return firstOrNone(getAllInstances(cls, name))

def Timed(fn: t.Callable[[t.List[t.Any]], None]) -> t.Callable[..., None]:
    """Runs & Times the given function, outputting how long the tests took"""
    @wraps(fn)
    def inner(*args: t.List[t.Any], **kwargs: t.Dict[t.Any, t.Any]) -> None:
        start = datetime.now()
        fn(*args, **kwargs)
        end = datetime.now()
        print(f"Tests took: {end-start}")
    return inner

def Setup(fn: t.Callable[[t.Any], None]) -> t.Callable[[t.Any], None]:
    """This function will run before every test, use it to set instance variables for testing"""
    setattr(fn, '_setup', True)
    return fn

def Teardown(fn: t.Callable[[t.Any], None]) -> t.Callable[[t.Any], None]:
    """This function will run after every test, use it to clear down any instance variables"""
    setattr(fn, '_teardown', True)
    return fn

def Test(fn: t.Callable[[t.Any], bool]) -> t.Callable[[t.Any], bool]:
    """Any method decorated with this will be run as a test"""
    setattr(fn, '_test', True)
    return fn

class Case(t.Generic[T]):
    """This must be placed on any TestCases with a collection of tests to be run in"""
    def __init__(self, collection: t.List['TestCase']) -> None:
        self.collection = collection

    def __call__(self, cls: t.Callable[[], 'TestCase']) -> 'TestCase':
        instance = cls()
        self.collection.append(instance)
        return instance

class TestCase:
    """
    Any children of this will inherit the assertion methods:\n
    `assertTrue(expression: bool) -> bool`\n
    `assertFalse(expression: bool) -> bool`\n
    `assertEqual(expected: str | int, actual: str | int) -> bool`\n
    `assertNotEqual(expected: str | int, actual: str | int) -> bool`
    """
    _tests: t.List[t.Callable[[], bool]]
    _setup: t.Optional[t.Callable[[], None]]
    _teardown: t.Optional[t.Callable[[], None]]

    def assertTrue(self, expression: bool) -> bool:
        return expression
    
    def assertFalse(self, expression: bool) -> bool:
        return not expression
    
    def assertEqual(self, expected: t.Union[str, int], actual: t.Union[str, int]) -> bool:
        return expected == actual
    
    def assertNotEqual(self, expected: t.Union[str, int], actual: t.Union[str, int]) -> bool:
        return expected != actual

    def assertIsNone(self, item: t.Optional[t.Any]) -> bool:
        return item is None

    def assertIsNotNone(self, item: t.Optional[t.Any]) -> bool:
        return item is not None

    def __init__(self) -> None:
        self._tests = getAllInstances(self, '_test')
        self._setup = getFirstInstance(self, '_setup')
        self._teardown = getFirstInstance(self, '_teardown')

    def run(self) -> None:
        failing = []
        for test in self._tests:
            if self._setup: self._setup()
            passes = test()
            if self._teardown: self._teardown()
            if not passes: failing.append(test)
        
        if len(failing) == 0: return
        print('%s Failing' % self.__class__.__name__)
        for ft in failing:
            print('\t%s' % ft.__name__)

@Timed
def run(test_collection: t.List[TestCase]) -> None:
    print("Beginning Testing...")
    for unit in test_collection:
        unit.run()
    print("Testing Complete.")
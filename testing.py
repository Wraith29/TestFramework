from datetime import datetime

__all__ = [
    "TestCase",
    "Setup", 
    "Test", 
    "Teardown", 
    "run"
]

def firstOrNone(arr):
    return arr[0] if len(arr) != 0 else None

def get_all_attrs(instance, attr_name):
    return [
            getattr(instance, attr)
            for attr in dir(instance)
            if hasattr(getattr(instance, attr), attr_name)
        ]

def get_first_attr(instance, attr_name):
    return firstOrNone([
            getattr(instance, attr)
            for attr in dir(instance)
            if callable(getattr(instance, attr))
            and hasattr(getattr(instance, attr), attr_name)
        ])


def timed(fn):
    " This decorator will output the time taken to run tests "
    def inner(*args, **kwargs) -> None:
        start_time = datetime.now()
        fn(*args, **kwargs)
        end_time = datetime.now()
        diff = end_time-start_time
        print(f"Tests took: {diff}")
    return inner

def run_test(instance, tests, setup=None, teardown=None):
    failing = []
    for test in tests:
        if setup: setup()
        passes = test()
        if teardown: teardown()
        if not passes: failing.append(test)
    
    if len(failing) == 0: return
    print('%s Failing: ' % instance.__class__.__name__)
    for ft in failing:
        print("    %s" % ft.__name__)

def configure_instance(instance, tests, setup_func=None, teardown_func=None):
    instance.run = lambda: run_test(instance, tests, setup_func, teardown_func)
    instance.expectFalse = lambda res: not res
    instance.expectTrue = lambda res: res
    instance.expectEqual = lambda exp, act: exp == act
    instance.expectNotEqual = lambda exp, act: exp != act
    return instance

def TestCase(collection):
    """
    Decorate a class with this and fill it with `Test` decorated methods.
    :param `collection` is a collection of test cases to be run by the `run()` command
    """
    def outer(cls):
        instance = cls()
        tests = get_all_attrs(instance, 'test')
        setup_func = get_first_attr(instance, 'setup')
        teardown_func = get_first_attr(instance, 'teardown')

        collection.append(instance)
        return configure_instance(instance, tests, setup_func, teardown_func)
    return outer

def Setup(fn):
    """Do not name this function `setup`, it can be called anything else"""
    fn.setup = True
    return fn

def Test(fn):
    """Decorate a method with this to have it run as a unit test"""
    fn.test = True
    return fn

def Teardown(fn):
    """Do not name this function `teardown`, it can be called anything else"""
    fn.teardown = True
    return fn

@timed
def run(col):
    print("Starting Tests...")
    for unit in col:
        unit.run()
    print("Tests Finished.")
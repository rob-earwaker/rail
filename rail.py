from builtins import super

import functools


def identity(value):
    return value


def raise_exception(exception):
    raise exception


def ignore(value):
    pass


class Error(Exception):
    pass


class UnmatchedValueError(Error):
    def __init__(self, value):
        self.value = value
        super().__init__(str(value))


def match(*args):
    def get_map_function(value):
        for is_match, map_function in args:
            if is_match(value):
                return map_function
        raise UnmatchedValueError(value)
    return lambda error: get_map_function(error)(error)


def match_type(*args):
    return match(*[
        (lambda value, types=types: isinstance(value, types), map_function)
        for types, map_function in args
    ])


def new():
    return Rail.new()


def compose(*functions):
    return Rail.new().compose(*functions)


class Rail(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, arg):
        return self.function(arg)

    @classmethod
    def new(cls, function=identity):
        return Rail(function)

    def compose(self, *functions):
        def compose2(function1, function2):
            return lambda arg: function2(function1(arg))
        return Rail.new(functools.reduce(compose2, functions, self.function))

    def tee(self, *functions):
        def tee_function(arg):
            Rail.new().compose(*functions)(arg)
            return arg
        return self.compose(tee_function)

    def fold(self, fold_value, fold_error):
        def fold_function(arg, function=self.function):
            try:
                return fold_value(function(arg))
            except Error as error:
                return fold_error(error)
        return Rail.new(fold_function)

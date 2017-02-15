import functools


def identity(value):
    return value


def raise_exception(exception):
    raise exception


class Failure(Exception):
    pass


class UnmatchedValueFailure(Failure):
    def __init__(self, value):
        self.value = value
        super().__init__(str(value))


def match(*args):
    def get_map_function(value):
        for is_match, map_function in args:
            if is_match(value):
                return map_function
        raise UnmatchedValueFailure(value)
    return lambda failure: get_map_function(failure)(failure)


def match_type(*args):
    return match(**[
        (lambda value: isinstance(value, match_types), map_function)
        for match_types, map_function in args
    ])


class Rail(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, arg):
        return self.function(arg)

    @classmethod
    def new(cls):
        return Rail(identity)

    def compose(self, *functions):
        def compose2(function1, function2):
            return lambda arg: function2(function1(arg))
        return Rail(functools.reduce(compose2, functions, self.function))

    def tee(self, *functions):
        def tee_function(arg):
            Rail.new().compose(*functions)(arg)
            return arg
        return self.compose(tee_function)

    def fold(self, fold_success, fold_failure):
        def fold_function(function, arg):
            try:
                return fold_success(function(arg))
            except Failure as failure:
                return fold_failure(failure)
        function = self.function
        return Rail.new().compose(lambda arg: fold_function(function, arg))

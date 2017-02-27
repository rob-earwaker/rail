import functools
import inspect


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
        super(Error, self).__init__(str(value))


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


class CurriedFunction(object):
    def __init__(self, function, arg_count, args):
        self.function = function
        self.arg_count = arg_count
        self.args = args

    @classmethod
    def from_function(cls, function):
        argspec = inspect.getargspec(function)
        print(argspec.args)
        return cls(function, arg_count=len(argspec.args), args=())

    def __call__(self, *args):
        curry = self.add_args(*args)
        return curry if len(curry.args) < curry.arg_count else curry.execute()

    def add_args(self, *args):
        return CurriedFunction(self.function, self.arg_count, self.args + args)

    def execute(self):
        return self.function(*self.args)


def curried(function):
    return CurriedFunction.from_function(function)


def new():
    return Track.new()


def compose(*functions):
    return Track.new().compose(*functions)


class Track(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, arg):
        return self.function(arg)

    @classmethod
    def new(cls, function=identity):
        return Track(function)

    def compose(self, *functions):
        def compose2(function1, function2):
            return lambda arg: function2(function1(arg))
        return Track.new(functools.reduce(compose2, functions, self.function))

    def tee(self, *functions):
        def tee_function(arg):
            Track.new().compose(*functions)(arg)
            return arg
        return self.compose(tee_function)

    def fold(self, fold_value, fold_error):
        def fold_function(arg, function=self.function):
            try:
                return fold_value(function(arg))
            except Error as error:
                return fold_error(error)
        return Track.new(fold_function)

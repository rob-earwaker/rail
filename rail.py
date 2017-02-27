import copy
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


class Arguments(object):
    NONE = object()

    def __init__(self, args):
        self.args = args

    @classmethod
    def from_arg_names(cls, arg_names):
        return cls(args=[(name, cls.NONE) for name in arg_names])

    def add_arg(self, arg):
        index, name = next(
            (i, n) for i, (n, a) in enumerate(self.args) if a == self.NONE
        )
        self.args[index] = (name, arg)

    def add_named_arg(self, name, arg):
        index = next(
            i for i, (n, _) in enumerate(self.args) if n == name
        )
        self.args[index] = (name, arg)

    def add_args(self, *args, **kwargs):
        arguments = Arguments(copy.copy(self.args))
        for arg in args:
            arguments.add_arg(arg)
        for name, arg in kwargs.items():
            arguments.add_named_arg(name, arg)
        return arguments

    def all_present(self):
        return all(arg != self.NONE for _, arg in self.args)

    def values(self):
        return [arg for _, arg in self.args]


class Partial(object):
    def __init__(self, function, args):
        self.function = function
        self.args = args

    @classmethod
    def from_function(cls, function):
        argspec = inspect.getargspec(function)
        return cls(function, Arguments.from_arg_names(argspec.args))

    def __call__(self, *args, **kwargs):
        partial = Partial(self.function, self.args.add_args(*args, **kwargs))
        return partial.execute() if partial.args.all_present() else partial

    def execute(self):
        return self.function(*self.args.values())


def partial(function):
    return Partial.from_function(function)


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

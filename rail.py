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


class Arg(object):
    NO_VALUE = object()
    NO_DEFAULT = object()

    def __init__(self, name, default, value):
        self.name = name
        self.default = default
        self.value = value

    @classmethod
    def from_name(cls, name, default=NO_DEFAULT):
        return cls(name, default, value=Arg.NO_VALUE)

    def has_value(self):
        return self.value != Arg.NO_VALUE

    def has_value_or_default(self):
        return self.has_value() or self.default != Arg.NO_DEFAULT

    def value_or_default(self):
        return self.value if self.has_value() else self.default

    def with_value(self, value):
        return Arg(self.name, self.default, value)


class Args(object):
    def __init__(self, args):
        self.args = args

    @classmethod
    def from_argspec(cls, argspec):
        defaults = argspec.defaults if argspec.defaults is not None else ()
        non_default_arg_count = len(argspec.args) - len(defaults)
        arg_defaults = (Arg.NO_DEFAULT,) * non_default_arg_count + defaults
        return cls(
            args=[
                Arg.from_name(name, default)
                for name, default in zip(argspec.args, arg_defaults)
            ]
        )

    def apply_arg(self, value):
        arg_index = next(
            index for index, arg in enumerate(self.args) if not arg.has_value()
        )
        self.args[arg_index] = self.args[arg_index].with_value(value)

    def apply_named_arg(self, name, value):
        arg_index = next(
            index for index, arg in enumerate(self.args) if arg.name == name
        )
        self.args[arg_index] = self.args[arg_index].with_value(value)

    def apply_args(self, *args, **kwargs):
        arguments = Args(copy.copy(self.args))
        for arg in args:
            arguments.apply_arg(arg)
        for name, arg in kwargs.items():
            arguments.apply_named_arg(name, arg)
        return arguments

    def all_present(self):
        return all(arg.has_value_or_default() for arg in self.args)

    def values(self):
        return [arg.value_or_default() for arg in self.args]


class Partial(object):
    def __init__(self, function, args):
        self.function = function
        self.args = args

    @classmethod
    def from_function(cls, function):
        argspec = inspect.getargspec(function)
        return cls(function, Args.from_argspec(argspec))

    def __call__(self, *args, **kwargs):
        partial = Partial(self.function, self.args.apply_args(*args, **kwargs))
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

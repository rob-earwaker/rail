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


class PositionalArg(object):
    NO_VALUE = object()
    NO_DEFAULT = object()

    def __init__(self, name, default, value):
        self.name = name
        self.default = default
        self.value = value

    @classmethod
    def from_name(cls, name, default=NO_DEFAULT):
        return cls(name, default, value=PositionalArg.NO_VALUE)

    def has_value(self):
        return self.value != PositionalArg.NO_VALUE

    def has_value_or_default(self):
        return self.has_value() or self.default != PositionalArg.NO_DEFAULT

    def value_or_default(self):
        return self.value if self.has_value() else self.default

    def with_value(self, value):
        return PositionalArg(self.name, self.default, value)


class Args(object):
    def __init__(self, named_args, list_args, keyword_args):
        self.named_args = named_args
        self.list_args = list_args
        self.keyword_args = keyword_args

    @classmethod
    def from_argspec(cls, argspec):
        defaults = argspec.defaults if argspec.defaults is not None else ()
        non_default_arg_count = len(argspec.args) - len(defaults)
        arg_defaults = (
            (PositionalArg.NO_DEFAULT,) * non_default_arg_count + defaults
        )
        return cls(
            named_args=[
                PositionalArg.from_name(name, default)
                for name, default in zip(argspec.args, arg_defaults)
            ],
            list_args=(),
            keyword_args={}
        )

    def apply_args(self, *args, **kwargs):
        named_args = copy.copy(self.named_args)
        list_args = copy.copy(self.list_args)
        keyword_args = copy.copy(self.keyword_args)
        for value in args:
            update_index = next(
                (
                    index for index, arg in enumerate(named_args)
                    if not arg.has_value()
                ),
                None
            )
            if update_index is not None:
                arg = named_args[update_index]
                named_args[update_index] = arg.with_value(value)
            else:
                list_args += (value,)
        for name, value in kwargs.items():
            update_index = next(
                (
                    index for index, arg in enumerate(named_args)
                    if arg.name == name
                ),
                None
            )
            if update_index is not None:
                arg = named_args[update_index]
                named_args[update_index] = arg.with_value(value)
            else:
                keyword_args[name] = value
        return Args(named_args, list_args, keyword_args)

    def all_present(self):
        return all(arg.has_value_or_default() for arg in self.named_args)

    def named_arg_values(self):
        return tuple(arg.value_or_default() for arg in self.named_args)


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
        return self.function(
            *(self.args.named_arg_values() + self.args.list_args),
            **self.args.keyword_args
        )


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

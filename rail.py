import copy
import functools
import inspect


def identity(value):
    return value


def RAISE(error):
    raise error


def ignore(value):
    pass


def TRY(value, func, handle):
    try:
        return func(value)
    except Exception as error:
        return handle(error)


class Error(Exception):
    pass


class UnmatchedValueError(Error):
    def __init__(self, value):
        self.value = value
        super(Error, self).__init__(str(value))


def match(*args):
    def get_map_func(value):
        for is_match, map_func in args:
            if is_match(value):
                return map_func
        raise UnmatchedValueError(value)
    return lambda error: get_map_func(error)(error)


def match_type(*args):
    return match(*[
        (lambda value, types=types: isinstance(value, types), map_func)
        for types, map_func in args
    ])


class NamedArg(object):
    NO_VALUE = object()
    NO_DEFAULT = object()

    def __init__(self, name, default, value):
        self.name = name
        self.default = default
        self.value = value

    @classmethod
    def from_name(cls, name, default=NO_DEFAULT):
        return cls(name, default, value=NamedArg.NO_VALUE)

    def has_value(self):
        return self.value != NamedArg.NO_VALUE

    def has_value_or_default(self):
        return self.has_value() or self.default != NamedArg.NO_DEFAULT

    def value_or_default(self):
        return self.value if self.has_value() else self.default

    def with_value(self, value):
        return NamedArg(self.name, self.default, value)


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
            (NamedArg.NO_DEFAULT,) * non_default_arg_count + defaults
        )
        return cls(
            named_args=[
                NamedArg.from_name(name, default)
                for name, default in zip(argspec.args, arg_defaults)
            ],
            list_args=(),
            keyword_args={}
        )

    @staticmethod
    def get_index(named_args, is_match):
        return next(
            (index for index, arg in enumerate(named_args) if is_match(arg)),
            None
        )

    def apply_args(self, *args, **kwargs):
        named_args = copy.copy(self.named_args)
        list_args = copy.copy(self.list_args)
        keyword_args = copy.copy(self.keyword_args)
        for value in args:
            index = Args.get_index(named_args, lambda arg: not arg.has_value())
            if index is not None:
                named_args[index] = named_args[index].with_value(value)
            else:
                list_args += (value,)
        for name, value in kwargs.items():
            index = Args.get_index(named_args, lambda arg: arg.name == name)
            if index is not None:
                named_args[index] = named_args[index].with_value(value)
            else:
                keyword_args[name] = value
        return Args(named_args, list_args, keyword_args)

    def all_present(self):
        return all(arg.has_value_or_default() for arg in self.named_args)

    def named_arg_values(self):
        return tuple(arg.value_or_default() for arg in self.named_args)


class Partial(object):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    @classmethod
    def from_func(cls, func):
        return pipe(
            func,
            inspect.getargspec,
            Args.from_argspec,
            lambda args: cls(func, args)
        )

    def __call__(self, *args, **kwargs):
        return pipe(
            self.args.apply_args(*args, **kwargs),
            lambda args: Partial(self.func, args),
            lambda partial:
                partial.execute() if partial.args.all_present() else partial
        )

    def execute(self):
        return self.func(
            *(self.args.named_arg_values() + self.args.list_args),
            **self.args.keyword_args
        )


def partial(func):
    return Partial.from_func(func)


def compose(*funcs):
    return functools.reduce(
        lambda func1, func2: lambda arg: func2(func1(arg)), funcs, identity
    )


def pipe(value, *funcs):
    func = compose(*funcs)
    return func(value)


def branch(*funcs):
    return lambda arg: pipe(
        arg,
        compose(*funcs),
        lambda _: arg
    )


class Track(object):
    def __init__(self, func=identity):
        self.func = func

    def __call__(self, arg):
        return self.func(arg)

    def compose(self, *funcs):
        return Track(compose(self.func, *funcs))

    def fold(self, success_func, handle_func):
        return self.compose(success_func).handle(handle_func)

    def handle(self, *funcs):
        def handle_func(arg):
            return TRY(
                arg,
                self.func,
                match_type(
                    (Error, compose(*funcs)),
                    (Exception, RAISE)
                )
            )
        return Track(handle_func)

    def tee(self, *funcs):
        return self.compose(branch(*funcs))

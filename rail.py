import functools
import inspect


def identity(value):
    return value


def RAISE(exception=None):
    if exception is None:
        raise
    else:
        raise exception


def TRY(func, handle):
    def try_func(arg):
        try:
            return func(arg)
        except Exception as exception:
            return handle(exception)
    return try_func


class UnmatchedValueError(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__(str(value))


def match(*args):
    return lambda value: pipe(
        next(
            (map_func for is_match, map_func in args if is_match(value)),
            lambda _: pipe(value, UnmatchedValueError, RAISE)
        ),
        call_with(value)
    )


def match_type(*args):
    return match(*[
        (lambda value, types=types: isinstance(value, types), map_func)
        for types, map_func in args
    ])


def match_length(*args):
    return match(*[
        (
            lambda value, match_len=match_len: pipe(value, len, match_len),
            map_func
        )
        for match_len, map_func in args
    ])


class NamedArg(object):
    NO_VALUE = object()
    NO_DEFAULT = object()

    def __init__(self, name, default=NO_DEFAULT, value=NO_VALUE):
        self.name = name
        self.default = default
        self.value = value

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
    def from_func(cls, func):
        return pipe(
            inspect.getargspec(func),
            lambda argspec: pipe(
                argspec.defaults if argspec.defaults is not None else (),
                reversed,
                list,
                lambda rdefaults: pipe(
                    argspec.args,
                    reversed,
                    lambda rargs: [
                        NamedArg(name, rdefaults[index])
                        if len(rdefaults) > index else NamedArg(name)
                        for index, name in enumerate(rargs)
                    ]
                )
            ),
            reversed,
            list,
            lambda named_args: cls(named_args, list_args=(), keyword_args={})
        )

    def get_named_arg_index(self, is_match):
        return pipe(
            self.named_args,
            lambda args:
                (index for index, arg in enumerate(args) if is_match(arg)),
            lambda iterator: next(iterator, None)
        )

    def apply_named_arg(self, index, value):
        return pipe(
            self.named_args.copy(),
            tee(
                lambda named_args: pipe(
                    named_args.pop(index),
                    lambda arg: named_args.insert(index, arg.with_value(value))
                )
            ),
            lambda named_args: Args(
                named_args, self.list_args, self.keyword_args.copy()
            )
        )

    def apply_list_arg(self, value):
        return pipe(
            self.list_args + (value,),
            lambda list_args: Args(
                self.named_args.copy(), list_args, self.keyword_args.copy()
            )
        )

    def apply_keyword_arg(self, name, value):
        return pipe(
            self.keyword_args.copy(),
            tee(lambda keyword_args: keyword_args.update({name: value})),
            lambda keyword_args: Args(
                self.named_args.copy(), self.list_args, keyword_args
            )
        )

    def apply_arg(self, value):
        return pipe(
            self.get_named_arg_index(lambda arg: not arg.has_value()),
            lambda index: (
                self.apply_named_arg(index, value) if index is not None
                else self.apply_list_arg(value)
            )
        )

    def apply_kwarg(self, name, value):
        return pipe(
            self.get_named_arg_index(lambda arg: arg.name == name),
            lambda index: (
                self.apply_named_arg(index, value) if index is not None
                else self.apply_keyword_arg(name, value)
            )
        )

    def apply_args(self, *args):
        return functools.reduce(
            lambda args, value: args.apply_arg(value), args, self
        )

    def apply_kwargs(self, **kwargs):
        return functools.reduce(
            lambda args, name: args.apply_kwarg(name, kwargs[name]),
            kwargs,
            self
        )

    def apply(self, *args, **kwargs):
        return self.apply_args(*args).apply_kwargs(**kwargs)

    def all_present(self):
        return all(arg.has_value_or_default() for arg in self.named_args)

    def named_arg_values(self):
        return tuple(arg.value_or_default() for arg in self.named_args)

    def execute(self, func):
        args = self.named_arg_values() + self.list_args
        return func(*args, **self.keyword_args)


def partial(func, applied_args=None):
    @functools.wraps(func)
    def partial_func(*args, **kwargs):
        return pipe(
            Args.from_func(func) if applied_args is None else applied_args,
            lambda existing_args: existing_args.apply(*args, **kwargs),
            lambda new_args: (
                new_args.execute(func) if new_args.all_present()
                else partial(func, new_args)
            )
        )
    return partial_func


def compose(*funcs):
    return functools.reduce(
        lambda func1, func2: lambda arg: func2(func1(arg)), funcs, identity
    )


def pipe(value, *funcs):
    func = compose(*funcs)
    return func(value)


def tee(*funcs):
    return lambda arg: pipe(
        arg,
        compose(*funcs),
        lambda _: arg
    )


@partial
def call_with(value, func):
    return func(value)


@partial
def lt(value2, value1):
    return value1 < value2


@partial
def le(value2, value1):
    return value1 <= value2


@partial
def eq(value2, value1):
    return value1 == value2


@partial
def ne(value2, value1):
    return value1 != value2


@partial
def gt(value2, value1):
    return value1 > value2


@partial
def ge(value2, value1):
    return value1 >= value2


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
        return Track(TRY(self.func, handle=compose(*funcs)))

    def tee(self, *funcs):
        return self.compose(tee(*funcs))

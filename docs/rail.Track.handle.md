## `rail.Track.handle`

The [`rail.Track.handle`](#railtrackhandle) method allows for error handling on a [`rail.Track`](./rail.Track.md#railtrack). It can be supplied with zero or more functions, which are composed into a single error handling function.

On execution of the [`rail.Track`](./rail.Track.md#railtrack), any [`rail.Error`](./rail.Error.md#railerror) exception thrown by a function composed prior to the [`rail.Track.handle`](#railtrackhandle) method call will be caught and passed to the error handling function. Execution of the [`rail.Track`](./rail.Track.md#railtrack) then continues with the value returned by the error handling function. If no [`rail.Error`](./rail.Error.md#railerror) exception is thrown, the error handling function will not be called, and execution will continue with the return value of the last composed function.

```python
>>> import rail
>>>
>>> func = rail.Track().compose(
...     lambda value: value if value < 10 else rail.RAISE(rail.Error('value must be < 10')),
...     lambda value: value + 10
... ).handle(
...     lambda error: str(error),
...     lambda message: message.upper()
... ).compose(
...     lambda message: 'Result = {0}'.format(message)
... )
>>> func(4)
'Result = 14'
>>> func(16)
'Result = VALUE MUST BE < 10'
>>>
```

Note that any non-[`rail.Error`](./rail.Error.md#railerror) exception raised during execution of a function composed prior to the [`rail.Track.handle`](#railtrackhandle) method call will not be caught:

```python
>>> func = rail.Track().compose(
...     lambda value: rail.RAISE(ValueError(value))
... ).handle(
...     lambda error: 'Error handled successfully'
... )
>>> func('hello')
Traceback (most recent call last):
  ...
ValueError: hello
>>>
```

Note that the [`rail.Track.handle`](#railtrackhandle) method is equivalent to calling [`rail.Track.fold`](./rail.Track.fold.md#railtrackfold) with the [`rail.identity`](./rail.identity.md#railidentity) function as the success case, i.e. `rail.Track.handle(handle_error)` is equivalent to `rail.Track.fold(rail.identity, handle_error)`.



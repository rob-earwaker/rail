## `rail.Track.handle`

The [`rail.Track.handle`](#railtrackhandle) method allows for exception handling on a [`rail.Track`](./rail.Track.md#railtrack) object. It can be supplied with zero or more functions, which are composed into a single exception handling function.

On execution of the [`rail.Track`](./rail.Track.md#railtrack), any `Exception` thrown by a function composed prior to the [`rail.Track.handle`](#railtrackhandle) method call will be caught and passed to the composed exception handling function. Execution of the [`rail.Track`](./rail.Track.md#railtrack) then continues with the function's return value. If no `Exception` is thrown, the exception handling function will not be called, and execution will continue with the return value of the last composed function.

```python
>>> import rail
>>>
>>> func = rail.Track().compose(
...     lambda value: value if value < 10 else rail.RAISE(ValueError('value must be < 10')),
...     lambda value: value + 10
... ).handle(
...     lambda exception: str(exception),
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

Note that the [`rail.Track.handle`](#railtrackhandle) method is equivalent to calling [`rail.Track.fold`](./rail.Track.fold.md#railtrackfold) with the [`rail.identity`](./rail.identity.md#railidentity) function as the success case, i.e. `rail.Track.handle(handle_exception)` is equivalent to `rail.Track.fold(rail.identity, handle_exception)`.



## `rail.Track.fold`

The [`rail.Track.fold`](#railtrackfold) method allows for convergence of the success and error paths of a [`rail.Track`](./rail.Track.md#railtrack), and can therefore be used for error handling. It must be supplied with two arguments - a function to be executed in the success case, and a function to be executed in the error case. Note that calling [`rail.Track.fold`](#railtrackfold) does not execute the [`rail.Track`](./rail.Track.md#railtrack), it simply composes another function and returns the new [`rail.Track`](./rail.Track.md#railtrack) object.

On execution of the [`rail.Track`](./rail.Track.md#railtrack), any [`rail.Error`](./rail.Error.md#railerror) exception thrown by a function composed prior to the [`rail.Track.fold`](#railtrackfold) method call will be caught and passed to the error function. If no [`rail.Error`](./rail.Error.md#railerror) exception is thrown, the success function will be called with the return value of the last function in the composition prior to the [`rail.Track.fold`](#railtrackfold) method call. The [`rail.Track`](./rail.Track.md#railtrack) execution will then continue with the return value of either the success or error function. For this reason, it is recommended that the return values of the success and error functions are of the same type.

```python
>>> import rail
>>>
>>> func = rail.Track().compose(
...     lambda value: value if len(value) > 4 else rail.RAISE(rail.Error())
... ).fold(
...     lambda value: 'greater',
...     lambda error: 'less'
... ).compose(
...     lambda message: 'Length is {0} than 4.'.format(message)
... )
>>> func('hello')
'Length is greater than 4.'
>>> func('hi')
'Length is less than 4.'
>>>
```

Note that any non-[`rail.Error`](./rail.Error.md#railerror) exception raised during execution of a function composed prior to the [`rail.Track.fold`](#railtrackfold) method call will not be caught:

```python
>>> func(9)
Traceback (most recent call last):
  ...
TypeError: object of type 'int' has no len()
>>>
```

Note that the [`rail.Track.fold`](#railtrackfold) method is equivalent to calling [`rail.Track.compose`](./rail.Track.compose.md#railtrackcompose) with the success function followed by calling [`rail.Track.handle`](./rail.Track.handle.md#railtrackhandle) with the error function, i.e. `rail.Track.fold(success_func, error_func)` is equivalent to `rail.Track.compose(success_func).handle(error_func)`.

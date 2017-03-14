## `rail.TRY`

The [`rail.TRY`](#railtry) function provides a mechanism for guarding a function against exceptions. It accepts two arguments, the first of which is a function that requires guarding and the second is a function to handle any `Exception` raised during execution. The returned value is a function that can be called with a single argument, which executes the guarded function within a `try` block abd handles any raised `Exception` using the handle function in an `except` block. The result is either the result of the guarded function or the result of the exception handling function, depending on whether or not an `Exception` was raised.

```python
>>> import rail
>>>
>>> func = rail.TRY(
...     lambda value: 'length is {0}'.format(len(value)),
...     lambda exception: 'handled {0}'.format(type(exception).__name__)
... )
>>>
>>> func('hello')
'length is 5'
>>> func(18)
'handled TypeError'
>>>
```

To re-raise an exception, use the [`rail.RAISE`](./rail.RAISE.md#railraise) function:

```python
>>> logfile = []
>>>
>>> func = rail.TRY(
...     lambda value: 'length is {0}'.format(len(value)),
...     rail.compose(
...         # Do some logging
...         rail.tee(
...             lambda exception: type(exception).__name__,
...             lambda type_name: 'FATAL: {0} raised!'.format(type_name),
...             lambda message: logfile.append(message)
...         ),
...         # Re-raise the exception
...         lambda exception: rail.RAISE()
...     )
... )
>>>
>>> func(18)
Traceback (most recent call last):
  ...
TypeError: object of type 'int' has no len()
>>>
>>> logfile
['FATAL: TypeError raised!']
>>>
```

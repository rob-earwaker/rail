## `rail.TRY`

The [`rail.TRY`](#railtry) function provides a functional approach to executing a function within a `try-except` block. It accepts three arguments, the first is the input value that will be passed to the function, the second is the function to be executed within the `try` block and the third is a function to handle any `Exception` raised during execution within the `except` block. The returned value is either the result of the executed function or the result of the exception handling function, depending on whether or not an `Exception` was raised.

```python
>>> import rail
>>>
>>> rail.TRY(
...     'World',
...     lambda value: 'Hello, {0}!'.format(value),
...     lambda exception: 'handled exception: {0}'.format(exception)
... )
'Hello, World!'
>>>
>>> rail.TRY(
...     107,
...     lambda value: len(value),
...     lambda exception: 'handled {0}'.format(type(exception).__name__)
... )
'handled TypeError'
>>>
```

To re-raise an exception, use the [`rail.RAISE`](./rail.RAISE.md#railraise) function:

```python
>>> logfile = []
>>>
>>> rail.TRY(
...     107,
...     lambda value: len(value),
...     rail.compose(
...         rail.tee(
...             lambda exception: type(exception).__name__,
...             lambda type_name: 'FATAL: {0} raised!'.format(type_name),
...             lambda message: logfile.append(message)
...         ),
...         lambda exception: rail.RAISE()
...     )
... )
Traceback (most recent call last):
  ...
TypeError: object of type 'int' has no len()
>>>
>>> logfile
['FATAL: TypeError raised!']
>>>
```

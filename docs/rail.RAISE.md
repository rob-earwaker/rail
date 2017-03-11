## `rail.RAISE`

The [`rail.RAISE`](#railraise) function is a functional equivalent of the `raise` keyword. It accepts a single argument, which it will attempt to raise as an exception:

```python
>>> import rail
>>>
>>> rail.RAISE(KeyError('key'))
Traceback (most recent call last):
  ...
KeyError: 'key'
>>>
>>>
>>> rail.RAISE('not an exception')
Traceback (most recent call last):
  ...
TypeError: exceptions must derive from BaseException
>>>
```

The advantage of the [`rail.RAISE`](#railraise) function over the `raise` keyword is that it can be used in places where a `raise` statement would result in a `SyntaxError`, e.g. in a `lambda` or a function call:

```python
>>> validate = lambda value: value if value > 10 else raise ValueError(value)
Traceback (most recent call last):
  ...
SyntaxError: invalid syntax
>>>
>>> validate = lambda value: value if value > 10 else rail.RAISE(ValueError(value))
>>> validate(13)
13
>>> validate(8)
Traceback (most recent call last):
  ...
ValueError: 8
>>>
>>> rail.pipe(
...     'something went wrong',
...     rail.Error,
...     raise
Traceback (most recent call last):
  ...
SyntaxError: invalid syntax
>>>
>>> rail.pipe(
...     'something went wrong',
...     rail.Error,
...     rail.RAISE
... )
Traceback (most recent call last):
  ...
rail.Error: something went wrong
>>>
```

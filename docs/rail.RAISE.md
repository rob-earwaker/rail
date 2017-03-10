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

The advantage of the [`rail.RAISE`](#railraise) function over the `raise` keyword is that it can be used in places where a `raise` statement would not be possible, e.g. in a `lambda` or in a function composition chain:

```python
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
...     rail.RAISE
... )
Traceback (most recent call last):
  ...
rail.Error: something went wrong
>>>
```

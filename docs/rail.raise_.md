## `rail.raise_`

The [`rail.raise_`](#railraise_) function is a functional equivalent of the `raise` keyword and can be called with either one argument or no arguments. When called with one argument, the `raise` keyword will be used on the value provided:

```python
>>> import rail
>>>
>>> rail.raise_(KeyError('key'))
Traceback (most recent call last):
  ...
KeyError: 'key'
>>>
>>>
>>> rail.raise_('not an exception')
Traceback (most recent call last):
  ...
TypeError: exceptions must derive from BaseException
>>>
```

When called with no arguments, the exception in the current context will be re-raised:

```python
>>> try:
...     raise ValueError('value')
... except ValueError:
...     rail.raise_()
...
Traceback (most recent call last):
  ...
ValueError: value
>>>
```

The advantage of the [`rail.raise_`](#railraise_) function over the `raise` keyword is that it can be used in places where a `raise` statement would result in a `SyntaxError`, e.g. in a `lambda` or a function call:

```python
>>> validate = lambda value: value if value > 10 else raise ValueError(value)
Traceback (most recent call last):
  ...
SyntaxError: invalid syntax
>>>
>>> validate = lambda value: value if value > 10 else rail.raise_(ValueError(value))
>>> validate(13)
13
>>> validate(8)
Traceback (most recent call last):
  ...
ValueError: 8
>>>
>>> rail.pipe(
...     'something went wrong',
...     ValueError,
...     raise
Traceback (most recent call last):
  ...
SyntaxError: invalid syntax
>>>
>>> rail.pipe(
...     'something went wrong',
...     ValueError,
...     rail.raise_
... )
Traceback (most recent call last):
  ...
ValueError: something went wrong
>>>
```

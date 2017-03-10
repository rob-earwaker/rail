## `rail.Track.compose`

The [`rail.Track.compose`](#railtrackcompose) method allows composition of additional functions onto the function wrapped by a [`rail.Track`](./rail.Track.md#railtrack) object. Composition has the effect of chaining functions together such that on execution the return value of the first function is passed to the second, and the return value from the second is then passed to the third, and so on. Since functions in Python can only return a single value, every function provided in the composition must accept a single argument only. The return value of the [`rail.Track.compose`](#railtrackcompose) method is a new [`rail.Track`](./rail.Track.md#railtrack) object wrapping the composed function.

```python
>>> import rail
>>>
>>> def exclaim(message):
...     return '{0}!'.format(message)
...
>>> func = rail.Track().compose(
...     lambda name: 'Hello, {0}'.format(name),
...     exclaim
... )
>>> func('Dave')
'Hello, Dave!'
>>>
```

If the [`rail.Track.compose`](#railtrackcompose) method is called with no arguments, the result is equivalent to the original [`rail.Track`](./rail.Track.md#railtrack) object.

Arguments to the [`rail.Track.compose`](#railtrackcompose) method do not have to be a Python `function`, they can be any callable object that accepts a single argument:

```python
>>> class Repeater(object):
...     def __init__(self, repeats):
...         self.repeats = repeats
...     def __call__(self, value):
...         return value * self.repeats
...
>>> class Result(object):
...     def __init__(self, value):
...         self.value = value
...     def __str__(self):
...         return 'The result is: {0}'.format(str(self.value))
...     
>>> func = rail.Track().compose(
...     Repeater(3),
...     Result,
...     str
... )
>>> func('ha')
'The result is: hahaha'
>>>
```

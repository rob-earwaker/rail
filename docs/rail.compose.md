## `rail.compose`

The [`rail.compose`](#railcompose) function composes zero or more functions into a single function. Composition has the effect of chaining functions together such that on execution the return value of the first function is passed to the second, and the return value from the second is then passed to the third, and so on. Since functions in Python can only return a single value, every function provided in the composition, including the first, must accept a single argument only.

```python
>>> import rail
>>>
>>> def double(value):
...     return value * 2
...     
>>> func = rail.compose(
...     double,
...     lambda value: value + 3
... )
>>> func(4)
11
>>>
```

If [`rail.compose`](#railcompose) is called with no functions, the result is equal to the [`rail.identity`](./rail.identity.md#railidentity) function:

```python
>>> func = rail.compose()
>>> func == rail.identity
True
>>> func('hello!')
'hello!'
>>>
```

Arguments to the [`rail.compose`](#railcompose) function do not have to be a Python `function`, they can be any callable object that accepts a single argument:

```python
>>> class Multiplier(object):
...     def __init__(self, multiplier):
...         self.multiplier = multiplier
...     def __call__(self, value):
...         return value * self.multiplier
...
>>> class Container(object):
...     def __init__(self, value):
...         self.value = value
...     def __repr__(self):
...         return 'Container(value={0})'.format(repr(self.value))
...     
>>> func = rail.compose(
...     int,
...     Multiplier(5),
...     Container
... )
>>> func(12.472)
Container(value=60)
>>>
```

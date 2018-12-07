## `rail.match`

The [`rail.match`](#railmatch) function provides an expressive way to map a value in different ways depending on the value itself, similar to a `switch` statement in other programming languages. It accepts zero or more match statements, each of which must be a `tuple` consisting of two single-argument functions, both of which will be passed the value being matched on. The first function in each match statement must return a 'truthy' value indicating when the match is successful for a given value, and the second function is responsible for mapping the given value once the match has been identified. The return value of the [`rail.match`](#railmatch) function is a new function that accepts a single argument. When this function is executed with a value, the value will be passed to each match statement in turn. When a successful match is found, the mapping function in that match statement will be applied to the value and the result will be returned.

```python
>>> import rail
>>>
>>> func = rail.match(
...     (lambda value: value > 0, lambda value: '{0} is positive'.format(value)),
...     (lambda value: value < 0, lambda value: '{0} is negative'.format(value)),
...     (lambda value: value == 0, lambda _: 'value is zero')
... )
>>>
>>> func(18.4)
'18.4 is positive'
>>> func(-0.6)
'-0.6 is negative'
>>> func(0)
'value is zero'
>>>
```

> TIP: The match statements above could be simplified using the [`rail.gt`](./rail.gt.md#railgt), [`rail.lt`](./rail.lt.md#raillt) and [`rail.eq`](./rail.eq.md#raileq) functions, e.g. `lambda value: value > 0` could be replaced with `rail.gt(0)`. In fact, the mapping functions could also be simplified, e.g. `lambda value: '{0} is positive'.format(value)` could be replaced with `'{0} is positive'.format`.

Note that since the match statements are checked in order, only the first match will be used even if multiple statements match the input value:

```python
>>> func = rail.match(
...     (lambda value: len(value) == 0, lambda _: 'length is zero'),
...     (lambda value: len(value) == 1, lambda _: 'length is one'),
...     (lambda value: len(value) > 0, lambda _: 'length is greater than zero')
... )
>>>
>>> func([])
'length is zero'
>>> func([0])
'length is one'
>>> func([0, 1, 2])
'length is greater than zero'
>>>
```

If none of the match statements match the input value, an [`rail.UnmatchedValueError`](./rail.UnmatchedValueError.md#railunmatchedvalueerror) will be raised.

```python
>>> fruit = ['banana', 'orange', 'apple']
>>> vegetables = ['potato', 'carrot', 'onion']
>>>
>>> func = rail.match(
...     (lambda value: value in fruit, lambda value: '{0} is a fruit'.format(value)),
...     (lambda value: value in vegetables, lambda value: '{0} is a vegetable'.format(value))
... )
>>>
>>> func('apple')
'apple is a fruit'
>>> func('carrot')
'carrot is a vegetable'
>>> func('chicken')
Traceback (most recent call last):
  ...
rail.UnmatchedValueError: chicken
>>>
```

In most cases it's useful to add a default match statement, which can always raise a custom exception if needs be. This removes the need to handle the [`rail.UnmatchedValueError`](./rail.UnmatchedValueError.md#railunmatchedvalueerror) exception.

```python
>>> func = rail.match(
...     (lambda value: value in fruit, lambda value: '{0} is a fruit'.format(value)),
...     (lambda value: value in vegetables, lambda value: '{0} is a vegetable'.format(value)),
...     (lambda _: True, lambda value: '{0} is not a vegetable or a fruit'.format(value))
... )
>>>
>>> func('bread')
'bread is not a vegetable or a fruit'
>>>
>>> class UnknownFoodTypeError(Exception):
...     pass
...
>>> func = rail.match(
...     (lambda value: value in fruit, lambda value: '{0} is a fruit'.format(value)),
...     (lambda value: value in vegetables, lambda value: '{0} is a vegetable'.format(value)),
...     (lambda _: True, lambda value: rail.raise_(UnknownFoodTypeError(value)))
... )
>>>
>>> func('bean')
Traceback (most recent call last):
  ...
UnknownFoodTypeError: bean
>>>
```

## `rail.match_type`

The [`rail.match_type`](#railmatch_type) function is a convenience function to allow easier matching of values by `type` then the basic [`rail.match`](./rail.match.md#railmatch) function. Similar to [`rail.match`](./rail.match.md#railmatch), the arguments for [`rail.match_type`](#railmatch_type) are a sequence of `tuple` arguments, however instead of a function returning a 'truthy' value as the first element of each tuple the function instead expects one or more types. A match is successful if the result of `isinstance` returns `True` for the types provided, i.e. `rail.match_type((types, map_func))` is equivalent to `rail.match((lambda value: isinstance(value, types), map_func))`.

```python
>>> import rail
>>>
>>> func = rail.match_type(
...     (str, lambda value: '{0} is a string'.format(value)),
...     ((int, float), lambda value: '{0} is a number'.format(value))
... )
>>>
>>> func('hello')
'hello is a string'
>>> func(9.6)
'9.6 is a number'
>>>
```

As with the [`rail.match`](./rail.match.md#railmatch) function, any unmatched values will result in an [`rail.UnmatchedValueError`](./rail.UnmatchedValueError.md#railunmatchedvalueerror) exception being raised. To prevent this, add a default match statement:

```python
>>> func = rail.match_type(
...     (str, lambda value: '{0} is a string'.format(value)),
...     ((int, float), lambda value: '{0} is a number'.format(value)),
...     (object, lambda value: '{0} has an unknown type'.format(value))
... )
>>>
>>> func({})
'{} has an unknown type'
>>>
```

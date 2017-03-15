## `rail.match_length`

The [`rail.match_length`](#railmatch_length) function is a convenience function to allow easier matching of values by length then the basic [`rail.match`](./rail.match.md#railmatch) function. Similar to [`rail.match`](./rail.match.md#railmatch), the arguments for [`rail.match_length`](#railmatch_length) are a sequence of `tuple` arguments, however the argument to the first element of each tuple is the length of the value being matched on rather than the value itself, i.e. `rail.match_length((is_match, map_func))` is equivalent to `rail.match((lambda value: is_match(len(value)), map_func))`.

```python
>>> import rail
>>>
>>> func = rail.match_length(
...     (lambda length: length < 6, lambda value: '"{0}" is a short word'.format(value)),
...     (lambda length: length > 8, lambda value: '"{0}" is a long word'.format(value))
... )
>>>
>>> func('hello')
'"hello" is a short word'
>>> func('fantastic')
'"fantastic" is a long word'
>>>
```

> TIP: The match statements above could be simplified using the [`rail.lt`](./rail.lt.md#raillt) and [`rail.gt`](./rail.gt.md#railgt) functions, e.g. `lambda length: langth < 6` could be replaced with `rail.lt(6)`.

As with the [`rail.match`](./rail.match.md#railmatch) function, any unmatched values will result in an [`rail.UnmatchedValueError`](./rail.UnmatchedValueError.md#railunmatchedvalueerror) exception being raised. To prevent this, add a default match statement:

```python
>>> func = rail.match_length(
...     (lambda length: length < 6, lambda value: '"{0}" is a short word'.format(value)),
...     (lambda length: length > 8, lambda value: '"{0}" is a long word'.format(value)),
...     (lambda _: True, lambda value: '"{0}" is neither a short word nor a long word'.format(value))
... )
>>>
>>> func('awesome')
'"awesome" is neither a short word nor a long word'
>>>
```

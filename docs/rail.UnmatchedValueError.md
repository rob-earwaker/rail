## `rail.UnmatchedValueError`

An [`rail.UnmatchedValueError`](#railunmatchedvalueerror) is raised when the function returned by one of the following match functions is passed a value that doesn't match any of the match statements:

- [`rail.match`](./rail.match.md#railmatch)
- [`rail.match_length`](./rail.match_length.md#railmatch_length)
- [`rail.match_type`](./rail.match_type.md#railmatch_type)

```python
>>> import rail
>>>
>>> func = rail.match(
...     (lambda value: value == 0, lambda _: 'value is zero')
... )
>>>
>>> func(0)
'value is zero'
>>> func(1)
Traceback (most recent call last):
  ...
rail.UnmatchedValueError: 1
>>>
```

Note that when creating a match function it is recommended that a default match statement is included to prevent an [`rail.UnmatchedValueError`](#railunmatchedvalueerror) being raised:

```python
>>> func = rail.match(
...     (lambda _: True, lambda _: 'no matches')
... )
>>> func(9)
'no matches'
>>>
>>> func = rail.match_length(
...     (lambda _: True, lambda _: 'no matches')
... )
>>> func([0, 1, 2])
'no matches'
>>>
>>> func = rail.match_type(
...     (object, lambda _: 'no matches')
... )
>>> func('hello')
'no matches'
>>>
```

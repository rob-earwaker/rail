## `rail.not_`

The [`rail.not_`](#railnot_) function is equivalent to the `not` keyword, i.e. `not value` is equivalent to `rail.not_(value)`. It's useful in situations where the `not` keyword needs to be applied in a functional way, e.g. as part of a function composition, as it saves writing the equivalent lambda function: `lambda value: not value`.

```python
>>> import rail
>>>
>>> rail.pipe(
...     [True, True, False, True],
...     lambda items: map(rail.not_, items),
...     list
... )
[False, False, True, False]
>>>
```

Usage in a non-functional way is not recommended as the `not value` syntax is almost always clearer in these cases, but it is still possible:

```python
>>> rail.not_(True)
False
>>>
>>> rail.not_([])
True
>>>
```

## `rail.lt`

The [`rail.lt`](#raillt) function is a functional equivalent of the `<` comparison operator. In order to make it expressive when used as part of a function composition, the argument order is reversed, i.e. `value1 < value2` is equivalent to `rail.lt(value2, value1)`, and it supports partial application through the [`rail.partial`](./rail.partial.md#railpartial) decorator:

```python
>>> import rail
>>>
>>> rail.pipe(6, rail.lt(8))
True
>>> rail.pipe(4, rail.lt(2))
False
>>>
```

Note that because the argument order is reversed, usage outside a function composition is not recommended as the `<` operator is almost always clearer in these cases, but it is still possible:

```python
>>> rail.lt(9, 0)
True
>>> rail.lt(7, 13)
False
>>>
```

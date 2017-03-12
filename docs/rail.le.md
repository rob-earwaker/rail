## `rail.le`

The [`rail.le`](#raille) function is a functional equivalent of the `<=` comparison operator. In order to make it expressive when used as part of a function composition, the argument order is reversed, i.e. `value1 <= value2` is equivalent to `rail.le(value2, value1)`, and it supports partial application through the [`rail.partial`](./rail.partial.md#railpartial) decorator:

```python
>>> import rail
>>>
>>> rail.pipe(2, rail.le(10))
True
>>> rail.pipe(2, rail.le(2))
True
>>> rail.pipe(5, rail.le(4))
False
>>>
```

Note that because the argument order is reversed, usage outside a function composition is not recommended as the `<=` operator is almost always clearer in these cases, but it is still possible:

```python
>>> rail.le(17, 6)
True
>>> rail.le(17, 17)
True
>>> rail.le(8, 14)
False
>>>
```

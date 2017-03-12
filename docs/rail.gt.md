## `rail.gt`

The [`rail.gt`](#railgt) function is a functional equivalent of the `>` comparison operator. In order to make it expressive when used as part of a function composition, the argument order is reversed, i.e. `value1 > value2` is equivalent to `rail.gt(value2, value1)`, and it supports partial application through the [`rail.partial`](./rail.partial.md#railpartial) decorator:

```python
>>> import rail
>>>
>>> rail.pipe(4, rail.gt(1))
True
>>> rail.pipe(7, rail.gt(14))
False
>>>
```

Note that because the argument order is reversed, usage outside a function composition is not recommended as the `>` operator is almost always clearer in these cases, but it is still possible:

```python
>>> rail.gt(3, 4)
True
>>> rail.gt(11, 10)
False
>>>
```

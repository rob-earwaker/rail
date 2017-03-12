## `rail.ge`

The [`rail.ge`](#railge) function is a functional equivalent of the `>=` comparison operator. In order to make it expressive when used as part of a function composition, the argument order is reversed, i.e. `value1 >= value2` is equivalent to `rail.ge(value2, value1)`, and it supports partial application through the [`rail.partial`](./rail.partial.md#railpartial) decorator:

```python
>>> import rail
>>>
>>> rail.pipe(13, rail.ge(10))
True
>>> rail.pipe(6, rail.ge(6))
True
>>> rail.pipe(0, rail.ge(3))
False
>>>
```

Note that because the argument order is reversed, usage outside a function composition is not recommended as the `>=` operator is almost always clearer in these cases, but it is still possible:

```python
>>> rail.ge(16, 20)
True
>>> rail.ge(8, 8)
True
>>> rail.ge(10, 3)
False
>>>
```

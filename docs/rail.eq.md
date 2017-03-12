## `rail.eq`

The [`rail.eq`](#raileq) function is a functional equivalent of the `==` comparison operator. In order to make it expressive when used as part of a function composition, the argument order is reversed, i.e. `value1 == value2` is equivalent to `rail.eq(value2, value1)`, and it supports partial application through the [`rail.partial`](./rail.partial.md#railpartial) decorator:

```python
>>> import rail
>>>
>>> value = object()
>>> rail.pipe(value, rail.eq(value))
True
>>> rail.pipe(value, rail.eq(object()))
False
>>>
```

Usage outside a function composition is not recommended as the `==` operator is almost always clearer in these cases, but it is still possible:

```python
>>> rail.eq(value, value)
True
>>> rail.eq(object(), value)
False
>>>
```

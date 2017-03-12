## `rail.eq`

The [`rail.eq`](#raileq) function is a functional equivalent of the `==` comparison operator, i.e. `rail.eq(value2, value1)` is equivalent to both `value1 == value2` and `value1.__eq__(value2)`:

```python
>>> import rail
>>>
>>> value = object()
>>> rail.eq(value, value)
True
>>> rail.eq(value, object())
False
>>>
```

The [`rail.eq`](#raileq) function also supports partial application through the [`rail.partial`](./rail.partial.md#railpartial) decorator:

```python
>>> equals5 = rail.eq(5)
>>> equals5(10)
False
>>> equals5(5)
True
>>>
```

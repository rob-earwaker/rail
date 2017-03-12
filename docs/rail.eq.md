## `rail.eq`

The [`rail.eq`](#raileq) function is a functional equivalent of the `==` comparison operator:

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

Note that the following expressions are all equivalent:

- `rail.eq(value2, value1)`
- `value1 == value2`
- `value1.__eq__(value2)`
- `operator.eq(value1, value2)`
- `operator.__eq__(value1, value2)`

The advantage of the [`rail.eq`](#raileq) function over the alternatives listed above is that it also supports partial application through the [`rail.partial`](./rail.partial.md#railpartial) decorator:

```python
>>> equals5 = rail.eq(5)
>>> equals5(10)
False
>>> equals5(5)
True
>>>
```

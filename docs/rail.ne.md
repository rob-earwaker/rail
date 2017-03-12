## `rail.ne`

The [`rail.ne`](#railne) function is a functional equivalent of the `!=` comparison operator, i.e. the following expressions are all equivalent:

- `rail.ne(value1, value2)`
- `value1 != value2`
- `value1.__ne__(value2)`
- `operator.ne(value1, value2)`
- `operator.__ne__(value1, value2)`

```python
>>> import rail
>>>
>>> value = object()
>>> rail.ne(value, value)
False
>>> rail.ne(value, object())
True
>>>
```

The advantage of the [`rail.ne`](#railne) function over the alternatives listed above is that it also supports partial application through the [`rail.partial`](./rail.partial.md#railpartial) decorator:

```python
>>> nonzero = rail.ne(0)
>>> nonzero(-7)
True
>>> nonzero(0)
False
>>>
```

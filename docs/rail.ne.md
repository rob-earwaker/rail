## `rail.ne`

The [`rail.ne`](#raileq) function is a functional equivalent of the `!=` comparison operator, i.e. `rail.ne(value1, value2)` is equivalent to both `value1 != value2` and `value1.__ne__(value2)`:

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

The [`rail.ne`](#raileq) function also supports partial application through the [`rail.partial`](./rail.partial.md#railpartial) decorator:

```python
>>> not_bob = rail.ne('Bob')
>>> not_bob('Ben')
True
>>> not_bob('Bob')
False
>>>
```

## `rail.call_with`

The [`rail.call_with`](#railcall_with) function is used to call a function with an argument. In order to make it expressive when used as part of a function composition the argument is provided first, followed by the function, i.e. `func(value)` is equivalent to `rail.call_with(value, func)`, and it supports partial application through the [`rail.partial`](./rail.partial.md#railpartial) decorator:

```python
>>> import rail
>>>
>>> rail.pipe(
...     str.lower,
...     rail.call_with('no need to SHOUT')
... )
'no need to shout'
>>>
>>> rail.pipe(
...     lambda value: value * 7,
...     rail.call_with(6)
... )
42
>>>
```

Note that because the argument order is reversed, usage outside a function composition is not recommended as the `func(value)` syntax is almost always clearer in these cases, but it is still possible:

```python
>>> rail.call_with('blue', lambda value: 'the sky is {0}'.format(value))
'the sky is blue'
>>> rail.call_with(5, lambda value: value + 23)
28
>>>
```

## `rail.pipe`

The [`rail.pipe`](#railpipe) function allows a value to be passed through a pipeline of zero or more functions, rather than composing the pipeline and then calling it with a value. The first argument to the [`rail.pipe`](#railpipe) function is the value to be passed through the pipeline, and subsequent arguments are the functions that will be composed into the pipeline:

```python
>>> import rail
>>>
>>> rail.pipe(
...     'LA',
...     lambda value: value * 4,
...     lambda value: value.lower()
... )
'lalalala'
>>>
```

Note that the [`rail.pipe`](#railpipe) function is equivalent to first composing the pipeline of functions using [`rail.compose`](./rail.compose.md#railcompose) and then calling the resulting function with the value, i.e. `rail.pipe(value, *funcs)` is equivalent to `rail.compose(*funcs)(value)`.

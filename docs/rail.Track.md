## `rail.Track`

A [`rail.Track`](#railtrack) object is a simple wrapper around a function that provides a variety of methods for modifying the wrapped function. A [`rail.Track`](#railtrack) object is callable in the same way as a function, but it always accepts a single argument only. Calling a [`rail.Track`](#railtrack) object executes the wrapped function.

The recommended way to create a [`rail.Track`](./rail.Track.md#railtrack) object is to call the constructor with no arguments:

```python
>>> import rail
>>>
>>> func = rail.Track()
>>> func
<rail.Track object at 0x...>
>>>
```

The returned object is equivalent to the [`rail.identity`](./rail.identity.md#railidentity) function wrapped in a [`rail.Track`](./rail.Track.md#railtrack) object:

```python
>>> func('hey')
'hey'
>>> func(9)
9
>>>
```

The following methods are available on a [`rail.Track`](./rail.Track.md#railtrack) object:

- [`rail.Track.compose`](./rail.Track.compose.md#railtrackcompose) - composes additional functions onto the wrapped function
- [`rail.Track.fold`](./rail.Track.fold.md#railtrackfold) - maps the success or error value of the wrapped function into a new value
- [`rail.Track.handle`](./rail.Track.handle.md#railtrackhandle) - maps an error that occurred during execution of the wrapped function into a new value
- [`rail.Track.tee`](./rail.Track.tee.md#railtracktee) - creates a new dead-end branch off the wrapped function

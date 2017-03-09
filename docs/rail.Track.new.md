## `rail.Track.new`

The [`rail.Track.new`](#railtracknew) class method is the recommended way to create a [`rail.Track`](./rail.Track.md#railtrack) object. It does not accept any arguments:

```python
>>> import rail
>>>
>>> func = rail.Track.new()
>>> func
<rail.Track object at 0x...>
>>>
```

The return value of the [`rail.Track.new`](#railtracknew) class method is equivalent to the [`rail.identity`](./rail.identity.md#railidentity) function wrapped in a [`rail.Track`](./rail.Track.md#railtrack) object:

```python
>>> func('hey')
'hey'
>>> func(9)
9
>>>
```

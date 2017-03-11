## `rail.identity`

The [`rail.identity`](#railidentity) function is a simple pass-through function, which accepts a single argument and returns it without modification:

```python
>>> import rail
>>>
>>> rail.identity(5)
5
>>>
>>> rail.identity('clock')
'clock'
>>>
>>> obj = object()
>>> rail.identity(obj) == obj
True
>>>
```

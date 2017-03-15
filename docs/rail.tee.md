## `rail.tee`

The [`rail.tee`](#railtee) function can be used to create a single-argument function that takes an input value, calls a function or chain of functions with that input value and then returns the same input value. This is typically used to add side effects to a function chain, where there is either no return value or the return value is not important.

```python
>>> import rail
>>>
>>> logfile = []
>>>
>>> func = rail.compose(
...     rail.tee(
...         lambda value: 'Converting {0} to upper case'.format(value),
...         lambda message: logfile.append(message)
...     ),
...     lambda value: value.upper(),
...     rail.tee(
...         lambda value: 'Result is {0}'.format(value),
...         lambda message: logfile.append(message)
...     )
... )
>>>
>>> func('dog')
'DOG'
>>> func('cat')
'CAT'
>>>
>>> for message in logfile:
...     message
...
'Converting dog to upper case'
'Result is DOG'
'Converting cat to upper case'
'Result is CAT'
>>>
```

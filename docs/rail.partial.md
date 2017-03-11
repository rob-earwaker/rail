## `rail.partial`

The [`rail.partial`](#railpartial) function is intended to be used as a decorator. It can be used on any function to allow partial application in a more expressive way than `functools.partial`. Arguments can be partially applied by simply calling the function with a subset of arguments. When the final argument is applied, the function is executed:

```python
>>> import rail
>>>
>>> @rail.partial
... def multiply(value1, value2):
...     return value1 * value2
...
>>> multiply(2, 4)
8
>>> triple = multiply(3)
>>> triple(4)
12
>>> triple(7)
21
>>>
```

As with any function call in Python, arguments can be applied out of order using the argument name:

```python
>>> @rail.partial
... def divide(dividend, divisor):
...     return dividend / divisor
...
>>> quarter = divide(divisor=4)
>>> quarter(10)
2.5
>>> quarter(44)
11.0
>>>
```

Any optional argument, i.e. any positional argument with a default value, any `*args` list argument and any `**kwargs` keyword argument, must be provided either before or along with the final non-default positional argument, as these are not required for function execution:

```python
>>> @rail.partial
... def print_args(arg1, arg2, arg3='default', *args, **kwargs):
...     return (arg1, arg2, arg3) + args + tuple(
...         '{0}={1}'.format(k, v) for k, v in sorted(kwargs.items())
...     )
...
>>> print_args('arg1', 'arg2')
('arg1', 'arg2', 'default')
>>>
>>> print_args('arg1', 'arg2', 'arg3')
('arg1', 'arg2', 'arg3')
>>> print_args('arg1', arg3='arg3')('arg2')
('arg1', 'arg2', 'arg3')
>>>
>>> print_args('arg1', 'arg2', 'arg3', 'arg4', 'arg5')
('arg1', 'arg2', 'arg3', 'arg4', 'arg5')
>>> print_args('arg1')('arg2', 'arg3', 'arg4', 'arg5')
('arg1', 'arg2', 'arg3', 'arg4', 'arg5')
>>>
>>> print_args('arg1', 'arg2', key1='kwarg1', key2='kwarg2')
('arg1', 'arg2', 'default', 'key1=kwarg1', 'key2=kwarg2')
>>> print_args('arg1', key1='kwarg1')('arg2', key2='kwarg2')
('arg1', 'arg2', 'default', 'key1=kwarg1', 'key2=kwarg2')
>>>
```

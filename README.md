[![Build Status](https://travis-ci.org/rob-earwaker/rail.svg?branch=master)](https://travis-ci.org/rob-earwaker/rail)
[![Coverage Status](https://coveralls.io/repos/github/rob-earwaker/rail/badge.svg?branch=master)](https://coveralls.io/github/rob-earwaker/rail?branch=master)

# rail
Railway oriented programming (ROP) in Python

## Concept
The key idea of ROP is that during execution you can either be on the success track or on the failure track. In other languages, this concept is usually encapsulated by a type that represents either a success or failure. In Python, a more standard way of dealing with failures is to simply raise an exception and leave it to some function higher up the call stack to deal with the error in whatever way is appropriate:

```python
>>> def validate(age):
...     if age < 0:
...         raise ValueError('{0} is an invalid age!'.format(age))
...     print('{0} is a valid age!'.format(age))
...
>>> validate(9)
9 is a valid age!
>>>
>>> validate(-4)
Traceback (most recent call last):
  ...
ValueError: -4 is an invalid age!
>>>
```

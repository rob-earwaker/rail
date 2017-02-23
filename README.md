[![Build Status](https://travis-ci.org/rob-earwaker/rail.svg?branch=master)](https://travis-ci.org/rob-earwaker/rail)
[![Coverage Status](https://coveralls.io/repos/github/rob-earwaker/rail/badge.svg?branch=master)](https://coveralls.io/github/rob-earwaker/rail?branch=master)

# rail
Railway oriented programming (ROP) in Python

## Concept
The key idea of ROP is that during execution you can either be on the success track or on the failure track. In other languages, this concept is usually encapsulated by an `Either` type (or similar) that represents either a success or failure, requiring that functions return an instance of `Either` containing either a success value or a failure value. In Python, a more standard way of dealing with failures is to simply raise an exception and leave it to some function higher up the call stack to deal with the error in whatever way is appropriate:

```python
>>> def validate(age):
...     if age < 0:
...         raise ValueError('{0} is an invalid age!'.format(age))
...     return age
...
>>> validate(35)
35
>>> validate(-4)
Traceback (most recent call last):
  ...
ValueError: -4 is an invalid age!
>>>
```

The `rail` package provides mechanisms for composing functions similar to the one above whilst providing convenient error handling options. As an example, the `validate` function can be composed using the `rail.compose` function:

```python
>>> import rail
>>> rail.compose(validate)
<rail.Rail object at 0x...>
>>>
```

A `rail.Rail` object is effectively just a wrapper around a function, and can be called directly to execute the function. In this case, we have only composed a single function, so the `rail.Rail` object behaves in exactly the same way as the `validate` function defined earlier:

```python
>>> validate2 = rail.compose(validate)
>>> validate2(7)
7
>>> validate(-22)
Traceback (most recent call last):
  ...
ValueError: -22 is an invalid age!
>>>
```
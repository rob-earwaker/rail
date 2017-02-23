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

The `rail` package provides mechanisms for composing functions similar to the one above into a ROP-style track, with convenient error handling options for failure cases. As an example, the `validate` function can be composed using the `rail.compose` function:

```python
>>> import rail
>>> track = rail.compose(validate)
>>> track
<rail.Track object at 0x...>
>>>
```

A `rail.Track` object is effectively just a wrapper around a function, and can be called directly to execute the function. In this case, we have only composed a single function, so the `rail.Track` object behaves in exactly the same way as the `validate` function defined earlier:

```python
>>> track(7)
7
>>> track(-22)
Traceback (most recent call last):
  ...
ValueError: -22 is an invalid age!
>>>
```

In order to add error handling to our track, we need to the `validate` function to throw an exception that the `rail.Track` object will recognise. The `rail` package defines a custom `rail.Error` exception for this purpose.

```python
>>> def validate(age):
...     if age < 0:
...         raise rail.Error('{0} is an invalid age!'.format(age))
...     return age
...
>>>
```

Note that by default a track has no error handling:

```python
>>> track = rail.compose(validate)
>>> track(-13)
Traceback (most recent call last):
  ...
rail.Error: -13 is an invalid age!
>>>
```

To add an error handling function onto a track, use the `rail.Track.fold` method. This must be called with two arguments, the first being a function to handle the success case and the second a function to handle the error case. When the track is executed, only one of these functions will be called based on whether a `rail.Error` has been raised, and the track will continue to execute with the result of this function:

```python
>>> track = rail.compose(validate).fold(
...     lambda value: '{0} is a valid age!'.format(value),
...     lambda error: str(error)
... )
>>> track(65)
'65 is a valid age!'
>>> track(-102)
'-102 is an invalid age!'
>>>
```

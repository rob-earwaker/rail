[![Build Status](https://travis-ci.org/rob-earwaker/rail.svg?branch=master)](https://travis-ci.org/rob-earwaker/rail)
[![Coverage Status](https://coveralls.io/repos/github/rob-earwaker/rail/badge.svg?branch=master)](https://coveralls.io/github/rob-earwaker/rail?branch=master)

# `rail`
Railway oriented programming (ROP) in Python

## Concept
The key idea of ROP is that during execution you can either be on the success track or on the failure track. In other languages, this concept is usually encapsulated by an `Either` type (or similar) that represents either a success or failure, requiring that functions return an instance of `Either` containing either a success value or a failure value. In Python, a more standard way of dealing with failures is to simply raise an exception and leave it to some function higher up the call stack to deal with the error in whatever way is appropriate:

```python
>>> def validate_age(age):
...     if age < 0:
...         raise ValueError('{0} is an invalid age!'.format(age))
...     return age
...
>>> validate_age(35)
35
>>> validate_age(-4)
Traceback (most recent call last):
  ...
ValueError: -4 is an invalid age!
>>>
```

The `rail` package provides mechanisms for composing functions similar to the one above into a ROP-style track, with convenient error handling options for failure cases. As an example, the `validate_age` function can be composed using the [`rail.compose`](#railcompose) function:

```python
>>> import rail
>>>
>>> handle_age = rail.compose(validate_age)
>>> handle_age
<rail.Track object at 0x...>
>>>
```

A `rail.Track` object is effectively just a wrapper around a function, and can be called directly to execute the function. In this case, we have only composed a single function, so the `rail.Track` object behaves in exactly the same way as the `validate_age` function defined earlier:

```python
>>> handle_age(7)
7
>>> handle_age(-22)
Traceback (most recent call last):
  ...
ValueError: -22 is an invalid age!
>>>
```

In order to add error handling to our track, we need the `validate_age` function to throw an exception that the `rail.Track` object will recognise. The `rail` package defines a custom `rail.Error` exception for this purpose.

```python
>>> def validate_age(age):
...     if age < 0:
...         raise rail.Error('{0} is an invalid age!'.format(age))
...     return age
...
>>>
```

Note that by default a track has no error handling:

```python
>>> handle_age = rail.compose(validate_age)
>>> handle_age(-13)
Traceback (most recent call last):
  ...
rail.Error: -13 is an invalid age!
>>>
```

To add an error handling function onto a track, use the `rail.Track.fold` method. This must be called with two arguments, the first being a function to handle the success case and the second a function to handle the error case. When the track is executed, only one of these functions will be called based on whether a `rail.Error` has been raised, and the track will continue to execute with the result of this function:

```python
>>> handle_age = rail.compose(validate_age).fold(
...     lambda value: '{0} is a valid age!'.format(value),
...     lambda error: str(error)
... )
>>> handle_age(65)
'65 is a valid age!'
>>> handle_age(-102)
'-102 is an invalid age!'
>>>
```

The example above is fairly simplistic. Lets create a slightly more complicated track:

```python
>>> import datetime
>>> import re
>>>
>>> import rail
>>>
>>> class DateOfBirthParsingError(rail.Error):
...     def __init__(self, value):
...         message = '{0} is an invalid date of birth'.format(value)
...         super(DateOfBirthParsingError, self).__init__(message)
...
>>> def parse_date_of_birth(value):
...     pattern = r'^(\d{4}).(\d{2}).(\d{2})$'
...     match = re.search(pattern, value)
...     if not match:
...         raise DateOfBirthParsingError(value)
...     year = int(match.group(1))
...     month = int(match.group(2))
...     day = int(match.group(3))
...     return datetime.date(year, month, day)
...
>>> class NegativeAgeError(rail.Error):
...     def __init__(self, date):
...         message = 'Date of birth is before {0}'.format(date)
...         super(NegativeAgeError, self).__init__(message)
...
>>> def calculate_age(date, date_of_birth):
...     age = date - date_of_birth
...     if age.total_seconds() < 0:
...         raise NegativeAgeError(date)
...     return age
...
>>> millenium_age = rail.compose(
...     lambda value: parse_date_of_birth(value),
...     lambda dob: calculate_age(datetime.date(2000, 1, 1), dob)
... ).fold(
...     lambda age: 'Age on 1st Jan 2000 was {0} days'.format(age.days),
...     lambda error: 'ERROR: {0}'.format(error)
... ).compose(
...     lambda value: '{0}!!!'.format(value)
... )
>>> millenium_age('1965-04-06')
'Age on 1st Jan 2000 was 12688 days!!!'
>>> millenium_age('1965/01/01')
'Age on 1st Jan 2000 was 12783 days!!!'
>>> millenium_age('99/04/23')
'ERROR: 99/04/23 is an invalid date of birth!!!'
>>> millenium_age('2010-02-17')
'ERROR: Date of birth is before 2000-01-01!!!'
>>>
```

## `rail.compose`
The [`rail.compose`](#railcompose) function should be used to create new `rail.Track` objects by composing zero or more functions. Since functions in Python can only return a single value, every function provided in the composition, including the first, must accept a single argument only:

```python
>>> import rail
>>>
>>> func = rail.compose(
...     lambda value: value * 2,
...     lambda value: value + 3
... )
>>> func(4)
11
>>>
```

If [`rail.compose`](#railcompose) is called with no functions, the result is equivalent to a `rail.Track` composed with the `rail.identity` function only:

```python
>>> func = rail.compose()
>>> func('hello!')
'hello!'
>>>
```

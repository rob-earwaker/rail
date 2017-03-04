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

The [`rail`](#rail) package provides mechanisms for composing functions similar to the one above into a ROP-style track, with convenient error handling options for failure cases. As an example, the `validate_age` function can be composed using the [`rail.compose`](#railcompose) function:

```python
>>> import rail
>>>
>>> handle_age = rail.compose(validate_age)
>>> handle_age
<rail.Track object at 0x...>
>>>
```

A [`rail.Track`](#railtrack) object is effectively just a wrapper around a function, and can be called directly to execute the function. In this case, we have only composed a single function, so the [`rail.Track`](#railtrack) object behaves in exactly the same way as the `validate_age` function defined earlier:

```python
>>> handle_age(7)
7
>>> handle_age(-22)
Traceback (most recent call last):
  ...
ValueError: -22 is an invalid age!
>>>
```

In order to add error handling to our track, we need the `validate_age` function to throw an exception that the [`rail.Track`](#railtrack) object will recognise. The [`rail`](#rail) package defines a custom [`rail.Error`](#railerror) exception for this purpose.

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

To add an error handling function onto a track, use the [`rail.Track.fold`](#railtrackfold) method. This must be called with two arguments, the first being a function to handle the success case and the second a function to handle the error case. When the track is executed, only one of these functions will be called based on whether a [`rail.Error`](#railerror) has been raised, and the track will continue to execute with the result of this function:

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

The [`rail.compose`](#railcompose) function composes zero or more functions and returns a new [`rail.Track`](#railtrack) object. Composition has the effect of chaining functions together such that on execution the return value of the first function is passed to the second, and the return value from the second is then passed to the third, and so on. Since functions in Python can only return a single value, every function provided in the composition, including the first, must accept a single argument only. If [`rail.compose`](#railcompose) is called with no functions, the result is equivalent to a [`rail.Track`](#railtrack) composed with the [`rail.identity`](#railidentity) function only.

```python
>>> import rail
>>>
>>> func = rail.compose()
>>> func('hello!')
'hello!'
>>>
>>> func = rail.compose(
...     lambda value: value * 2,
...     lambda value: value + 3
... )
>>> func(4)
11
>>>
```

## `rail.Track`
...


## `rail.Track.compose`
...


## `rail.Track.fold`

The [`rail.Track.fold`](#railtrackfold) method allows for convergence of the success and error paths of a [`rail.Track`](#railtrack), and can therefore be used for error handling. It must be supplied with two arguments - a function to be executed in the success case, and a function to be executed in the error case. Note that calling [`rail.Track.fold`](#railtrackfold) does not execute the [`rail.Track`](#railtrack), it simply composes another function and returns the new [`rail.Track`](#railtrack) object.

On execution of the [`rail.Track`](#railtrack), any [`rail.Error`](#railerror) exception thrown by a function composed prior to the [`rail.Track.fold`](#railtrackfold) method call will be caught and passed to the error function. If no [`rail.Error`](#railerror) exception is thrown, the success function will be called with the return value of the last function in the composition prior to the [`rail.Track.fold`](#railtrackfold) method call. The [`rail.Track`](#railtrack) execution will then continue with the return value of either the success or error function. For this reason, it is recommended that the return values of the success and error functions are of the same type. In the example below, both the [`rail.compose`](#railcompose) function and the [`rail.Track.compose`](#railtrackcompose) method are used to create the function compositions before and after the [`rail.Track.fold`](#railtrackfold) method call respectively. The [`rail.raise_exception`](#railraiseexception) function is also used to raise a [`rail.Error`](#railerror) from within the composed lambda function.

```python
>>> import rail
>>>
>>> func = rail.compose(
...     lambda value: value if len(value) > 4 else rail.raise_exception(rail.Error())
... ).fold(
...     lambda value: 'greater',
...     lambda error: 'less'
... ).compose(
...     lambda message: 'Length is {0} than 4.'.format(message)
... )
>>> func([0, 1, 2, 3, 4])
'Length is greater than 4.'
>>> func([0, 1])
'Length is less than 4.'
>>>
```

Note that any non-[`rail.Error`](#railerror) exception raised during execution of a function composed prior to the [`rail.Track.fold`](#railtrackfold) method call will not be caught:

```python
>>> func('hello!')
'Length is greater than 4.'
>>> func(9)
Traceback (most recent call last):
  ...
TypeError: object of type 'int' has no len()
>>>
```


## `rail.Error`
...


## `rail.identity`
...


## `rail.raise_exception`
...

## Concept

The key idea of ROP is that during execution you can either be on the success track or on the failure track. In other languages, this concept is usually encapsulated by an `Either` type (or similar) that represents either a success or failure, requiring that functions return an instance of `Either` containing either a success value or a failure value. In Python, a more standard way of dealing with failures is to simply raise an exception and leave it to some function higher up the call stack to deal with in whatever way is appropriate:

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

The [`rail`](./rail.md#rail) package provides mechanisms for composing functions similar to the one above into a ROP-style track, with convenient exception handling options for failure cases. As an example, the `validate_age` function can be composed using the [`rail.Track.compose`](./rail.Track.compose.md#railtrackcompose) function on a new [`rail.Track`](./rail.Track.md#railtrack) object:

```python
>>> import rail
>>>
>>> handle_age = rail.Track().compose(validate_age)
>>> handle_age
<rail.Track object at 0x...>
>>>
```

A [`rail.Track`](./rail.Track.md#railtrack) object is effectively just a wrapper around a function, and can be called directly to execute the function. In this case, we have only composed a single function, so the [`rail.Track`](./rail.Track.md#railtrack) object behaves in exactly the same way as the `validate_age` function defined earlier:

```python
>>> handle_age(7)
7
>>> handle_age(-22)
Traceback (most recent call last):
  ...
ValueError: -22 is an invalid age!
>>>
```

To add an exception handling function onto a track, use the [`rail.Track.handle`](./rail.Track.handle.md#railtrackhandle) method. This must be called with a single argument, which is a function that accepts a single argument. When the track is executed, any `Exception` raised during execution will be caught and passed to this function, and the track will continue to execute with the return value:

```python
>>> handle_age = rail.Track().compose(
...     validate_age,
...     lambda value: '{0} is a valid age!'.format(value)
... ).handle(
...     lambda exception: str(exception)
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
>>> class DateOfBirthParsingError(Exception):
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
>>> class NegativeAgeError(Exception):
...     def __init__(self, date):
...         message = 'Date of birth is after {0}'.format(date)
...         super(NegativeAgeError, self).__init__(message)
...
>>> def calculate_age(date, date_of_birth):
...     age = date - date_of_birth
...     if age.total_seconds() < 0:
...         raise NegativeAgeError(date)
...     return age
...
>>> millenium_age = rail.Track().compose(
...     lambda value: parse_date_of_birth(value),
...     lambda dob: calculate_age(datetime.date(2000, 1, 1), dob),
...     lambda age: 'Age on 1st Jan 2000 was {0} days'.format(age.days)
... ).handle(
...     lambda exception: 'ERROR: {0}'.format(exception)
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
'ERROR: Date of birth is after 2000-01-01!!!'
>>>
```

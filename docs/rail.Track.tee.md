## `rail.Track.tee`

The [`rail.Track.tee`](#railtracktee) method allows execution of functions on a dead-end branch off the current [`rail.Track`](./rail.Track#railtrack) object. Similar to the [`rail.Track.compose`](./rail.Track.compose.md#railtrackcompose) method, the [`rail.Track.tee`](#railtracktee) method takes a series of functions, the input of which will be the return value of the last composed function on the [`rail.Track`](./rail.Track#railtrack) object. The difference is that this same input value is returned once the branch has finished executing, instead of the return value of the final function in the branch. In the example below, the item passed to the function is passed to the function in the [`rail.Track.tee`](#railtracktee) method call as well as the function in the subsequent [`rail.Track.compose`](./rail.Track.compose.md#railtrackcompose) method call. The return values of the function in the [`rail.Track.tee`](#railtracktee) method call, which in this case is `None`, is ignored.

```python
>>> import rail
>>>
>>> basket = []
>>> func = rail.Track().tee(
...     lambda item: basket.append(item)
... ).compose(
...     lambda item: 'Added {0} to basket'.format(item)
... )
>>>
>>> func('orange')
'Added orange to basket'
>>> func('banana')
'Added banana to basket'
>>> basket
['orange', 'banana']
>>>
```

Errors raised by a function passed to the [`rail.Track.tee`](#railtracktee) method call halt execution of the [`rail.Track`](./rail.Track#railtrack) object in exactly the same way as any composed function:

```python
>>> basket = []
>>> func = rail.Track().tee(
...     lambda item: item if len(basket) < 2 else rail.RAISE(rail.Error('too many items')),
...     lambda item: basket.append(item)
... ).compose(
...     lambda item: 'Added {0} to basket'.format(item)
... )
>>> func('pear')
'Added pear to basket'
>>> func('melon')
'Added melon to basket'
>>> func('apple')
Traceback (most recent call last):
  ...
rail.Error: too many items
>>> basket
['pear', 'melon']
>>>
```

Note that the [`rail.Track.tee`](#railtracktee) method is equivalent to calling [`rail.Track.compose`](./rail.Track.compose.md#railtrackcompose) with the [`rail.tee`](./rail.tee.md#railtee) function, i.e. `rail.Track.tee(*funcs)` is equivalent to `rail.Track.compose(rail.tee(*funcs))`.

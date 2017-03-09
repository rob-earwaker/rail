## `rail.Track`

A [`rail.Track`](#railtrack) object is a simple wrapper around a function that provides a variety of methods for modifying the wrapped function. A [`rail.Track`](#railtrack) object is callable in the same way as a function, but it always accepts a single argument only. Calling a [`rail.Track`](#railtrack) object executes the wrapped function.

To create a [`rail.Track`](#railtrack) object, use the [`rail.Track.new`](./rail.Track.new.md#railtracknew) class method.

The following methods are available on a [`rail.Track`](#railtrack) object, all of which modify the wrapped function in some way and return a new [`rail.Track`](#railtrack) object wrapping the modified function:

- [`rail.Track.compose`](./rail.Track.compose.md#railtrackcompose) - composes additional functions onto the wrapped function
- [`rail.Track.fold`](./rail.Track.fold.md#railtrackfold) - maps the success or error value of the wrapped function into a new value
- [`rail.Track.handle`](./rail.Track.handle.md#railtrackhandle) - maps an error that occurred during execution of the wrapped function into a new value
- [`rail.Track.tee`](./rail.Track.tee.md#railtracktee) - creates a new dead-end branch off the wrapped function

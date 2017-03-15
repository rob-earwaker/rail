import sys
import traceback
import unittest
import unittest.mock

import rail


class TestIdentity(unittest.TestCase):
    def test_returns_input_value(self):
        value = unittest.mock.Mock()
        self.assertEqual(value, rail.identity(value))


class TestRaise(unittest.TestCase):
    def test_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            rail.RAISE(ValueError('exception'))
        self.assertEqual('exception', str(context.exception))

    def test_preserves_traceback_when_reraising_without_exception(self):
        def func(exception):
            raise exception
        try:
            try:
                func(ValueError('exception'))
            except ValueError:
                expected_exc_info = sys.exc_info()
                rail.RAISE()
        except ValueError:
            actual_exc_info = sys.exc_info()
        self.assertEqual(expected_exc_info[0], actual_exc_info[0])
        self.assertEqual(expected_exc_info[1], actual_exc_info[1])
        expected_tb = traceback.format_tb(expected_exc_info[2])
        actual_tb = traceback.format_tb(actual_exc_info[2])
        self.assertEqual(expected_tb, actual_tb[-len(expected_tb):])

    def test_preserves_traceback_when_reraising_with_exception(self):
        def func(exception):
            raise exception
        try:
            try:
                func(ValueError('exception'))
            except ValueError as exception:
                expected_exc_info = sys.exc_info()
                rail.RAISE(exception)
        except ValueError:
            actual_exc_info = sys.exc_info()
        self.assertEqual(expected_exc_info[0], actual_exc_info[0])
        self.assertEqual(expected_exc_info[1], actual_exc_info[1])
        expected_tb = traceback.format_tb(expected_exc_info[2])
        actual_tb = traceback.format_tb(actual_exc_info[2])
        self.assertEqual(expected_tb, actual_tb[-len(expected_tb):])


class TestTry(unittest.TestCase):
    def test_no_exception_raised(self):
        input = unittest.mock.Mock()
        expected_value = unittest.mock.Mock()
        func = unittest.mock.Mock(return_value=expected_value)
        handle = unittest.mock.Mock()
        self.assertEqual(expected_value, rail.TRY(func, handle)(input))
        func.assert_called_once_with(input)
        handle.assert_not_called()

    def test_exception_raised(self):
        input = unittest.mock.Mock()
        exception = ValueError('value')
        func = unittest.mock.Mock(side_effect=lambda _: rail.RAISE(exception))
        output = unittest.mock.Mock()
        handle = unittest.mock.Mock(return_value=output)
        self.assertEqual(output, rail.TRY(func, handle)(input))
        func.assert_called_once_with(input)
        handle.assert_called_once_with(exception)


class TestMatch(unittest.TestCase):
    def test_no_match_statements_provided(self):
        value = unittest.mock.Mock()
        with self.assertRaises(rail.UnmatchedValueError) as context:
            rail.match()(value)
        self.assertEqual(value, context.exception.value)

    def test_value_unmatched_by_all_match_statements(self):
        value = unittest.mock.Mock()
        with self.assertRaises(rail.UnmatchedValueError) as context:
            match = rail.match(
                (lambda _: False, lambda _: unittest.mock.Mock()),
                (lambda _: False, lambda _: unittest.mock.Mock()),
                (lambda _: False, lambda _: unittest.mock.Mock())
            )
            match(value)
        self.assertEqual(value, context.exception.value)

    def test_value_matches_single_match_statement(self):
        expected_value = unittest.mock.Mock()
        match = rail.match(
            (lambda _: False, lambda _: unittest.mock.Mock()),
            (lambda _: True, lambda _: expected_value),
            (lambda _: False, lambda _: unittest.mock.Mock())
        )
        self.assertEqual(expected_value, match(unittest.mock.Mock()))

    def test_value_matches_multiple_match_statements(self):
        expected_value = unittest.mock.Mock()
        match = rail.match(
            (lambda _: False, lambda _: unittest.mock.Mock()),
            (lambda _: True, lambda _: expected_value),
            (lambda _: True, lambda _: unittest.mock.Mock())
        )
        self.assertEqual(expected_value, match(unittest.mock.Mock()))


class TestMatchType(unittest.TestCase):
    def test_no_match_statements_provided(self):
        value = unittest.mock.Mock()
        with self.assertRaises(rail.UnmatchedValueError) as context:
            rail.match_type()(value)
        self.assertEqual(value, context.exception.value)

    def test_value_unmatched_by_all_match_statements(self):
        value = unittest.mock.Mock()
        with self.assertRaises(rail.UnmatchedValueError) as context:
            match = rail.match_type(
                (str, lambda _: unittest.mock.Mock()),
                (float, lambda _: unittest.mock.Mock()),
                (Exception, lambda _: unittest.mock.Mock())
            )
            match(value)
        self.assertEqual(value, context.exception.value)

    def test_value_matches_single_match_statement(self):
        expected_value = unittest.mock.Mock()
        match = rail.match_type(
            (int, lambda _: unittest.mock.Mock()),
            (unittest.mock.Mock, lambda _: expected_value),
            (dict, lambda _: unittest.mock.Mock())
        )
        self.assertEqual(expected_value, match(unittest.mock.Mock()))

    def test_value_matches_multiple_match_statements(self):
        expected_value = unittest.mock.Mock()
        match = rail.match_type(
            (bool, lambda _: unittest.mock.Mock()),
            (unittest.mock.Mock, lambda _: expected_value),
            (unittest.mock.Mock, lambda _: unittest.mock.Mock())
        )
        self.assertEqual(expected_value, match(unittest.mock.Mock()))

    def test_value_subclass_of_match_type(self):
        expected_value = unittest.mock.Mock()
        match = rail.match_type(
            (bool, lambda _: unittest.mock.Mock()),
            (object, lambda _: expected_value),
            (unittest.mock.Mock, lambda _: unittest.mock.Mock())
        )
        self.assertEqual(expected_value, match(unittest.mock.Mock()))


class TestMatchLength(unittest.TestCase):
    def test_no_match_statements_provided(self):
        value = unittest.mock.Mock()
        with self.assertRaises(rail.UnmatchedValueError) as context:
            rail.match_length()(value)
        self.assertEqual(value, context.exception.value)

    def test_value_unmatched_by_all_match_statements(self):
        value = unittest.mock.Mock()
        value.__len__ = unittest.mock.Mock(return_value=2)
        with self.assertRaises(rail.UnmatchedValueError) as context:
            match = rail.match_length(
                (rail.eq(8), lambda _: unittest.mock.Mock()),
                (rail.gt(3), lambda _: unittest.mock.Mock())
            )
            match(value)
        self.assertEqual(value, context.exception.value)

    def test_value_matches_single_match_statement(self):
        expected_value = unittest.mock.Mock()
        match = rail.match_length(
            (rail.lt(0), lambda _: unittest.mock.Mock()),
            (rail.eq(0), lambda _: expected_value),
            (rail.gt(0), lambda _: unittest.mock.Mock())
        )
        value = unittest.mock.Mock()
        value.__len__ = unittest.mock.Mock(return_value=0)
        self.assertEqual(expected_value, match(value))

    def test_value_matches_multiple_match_statements(self):
        expected_value = unittest.mock.Mock()
        match = rail.match_length(
            (rail.lt(0), lambda _: unittest.mock.Mock()),
            (rail.ge(0), lambda _: expected_value),
            (rail.eq(0), lambda _: unittest.mock.Mock())
        )
        value = unittest.mock.Mock()
        value.__len__ = unittest.mock.Mock(return_value=0)
        self.assertEqual(expected_value, match(value))


class TestPartial(unittest.TestCase):
    def test_func_with_no_args(self):
        @rail.partial
        def func():
            return 'value'
        self.assertEqual('value', func())

    def test_func_with_single_arg(self):
        @rail.partial
        def func(arg):
            return arg
        value = unittest.mock.Mock()
        self.assertEqual(value, func(value))

    def test_func_with_multiple_args(self):
        @rail.partial
        def func(arg1, arg2, arg3):
            return arg1, arg2, arg3
        val1 = unittest.mock.Mock()
        val2 = unittest.mock.Mock()
        val3 = unittest.mock.Mock()
        self.assertEqual((val1, val2, val3), func(val1, val2, val3))
        self.assertEqual((val1, val2, val3), func(val1)(val2, val3))
        self.assertEqual((val1, val2, val3), func(val1, val2)(val3))
        self.assertEqual((val1, val2, val3), func(val1)(val2)(val3))

    def test_func_with_arguments_applied_out_of_order(self):
        @rail.partial
        def func(arg1, arg2, arg3):
            return arg1, arg2, arg3
        val1 = unittest.mock.Mock()
        val2 = unittest.mock.Mock()
        val3 = unittest.mock.Mock()
        self.assertEqual((val1, val2, val3), func(arg2=val2)(val1, val3))
        self.assertEqual((val1, val2, val3), func(arg3=val3)(val1, val2))
        self.assertEqual(
            (val1, val2, val3), func(arg2=val2, arg3=val3)(val1)
        )
        self.assertEqual(
            (val1, val2, val3), func(arg3=val3)(arg2=val2)(val1)
        )
        self.assertEqual((val1, val2, val3), func(val1, arg3=val3)(val2))

    def test_func_with_default_arguments(self):
        @rail.partial
        def func(arg1, arg2, arg3='val3', arg4='val4'):
            return arg1, arg2, arg3, arg4
        val1 = unittest.mock.Mock()
        val2 = unittest.mock.Mock()
        val3 = unittest.mock.Mock()
        val4 = unittest.mock.Mock()
        self.assertEqual((val1, val2, 'val3', 'val4'), func(val1, val2))
        self.assertEqual((val1, val2, 'val3', 'val4'), func(val1)(val2))
        self.assertEqual(
            (val1, val2, val3, val4), func(val1, val2, val3, val4)
        )
        self.assertEqual(
            (val1, val2, val3, val4), func(val1)(val2, val3, val4)
        )
        self.assertEqual(
            (val1, val2, val3, val4), func(val1, arg3=val3)(val2, val4)
        )

    def test_func_with_default_arguments_only(self):
        @rail.partial
        def func(arg1='val1', arg2='val2'):
            return arg1, arg2
        val1 = unittest.mock.Mock()
        val2 = unittest.mock.Mock()
        self.assertEqual(('val1', 'val2'), func())
        self.assertEqual((val1, 'val2'), func(val1))
        self.assertEqual(('val1', val2), func(arg2=val2))
        self.assertEqual((val1, val2), func(val1, val2))

    def test_func_with_argument_list(self):
        @rail.partial
        def func(arg1, arg2, *args):
            return (arg1, arg2) + args
        val1 = unittest.mock.Mock()
        val2 = unittest.mock.Mock()
        val3 = unittest.mock.Mock()
        val4 = unittest.mock.Mock()
        self.assertEqual((val1, val2), func(val1, val2))
        self.assertEqual((val1, val2), func(val1)(val2))
        self.assertEqual(
            (val1, val2, val3, val4), func(val1, val2, val3, val4)
        )
        self.assertEqual(
            (val1, val2, val3, val4), func(val1)(val2, val3, val4)
        )

    def test_func_with_argument_list_only(self):
        @rail.partial
        def func(*args):
            return args
        val1 = unittest.mock.Mock()
        val2 = unittest.mock.Mock()
        self.assertEqual((), func())
        self.assertEqual((val1,), func(val1))
        self.assertEqual((val1, val2), func(val1, val2))

    def test_func_with_keyword_arguments(self):
        @rail.partial
        def func(arg1, arg2, **kwargs):
            return (arg1, arg2) + ((kwargs,) if kwargs else ())
        val1 = unittest.mock.Mock()
        val2 = unittest.mock.Mock()
        val3 = unittest.mock.Mock()
        val4 = unittest.mock.Mock()
        self.assertEqual((val1, val2), func(val1, val2))
        self.assertEqual((val1, val2), func(val1)(val2))
        self.assertEqual(
            (val1, val2, {'val3': val3, 'val4': val4}),
            func(val1, val2, val3=val3, val4=val4)
        )
        self.assertEqual(
            (val1, val2, {'val3': val3, 'val4': val4}),
            func(val1, val3=val3)(val2, val4=val4)
        )

    def test_func_with_keyword_arguments_only(self):
        @rail.partial
        def func(**kwargs):
            return kwargs
        val1 = unittest.mock.Mock()
        val2 = unittest.mock.Mock()
        self.assertEqual({}, func())
        self.assertEqual({'arg1': val1}, func(arg1=val1))
        self.assertEqual(
            {'arg1': val1, 'arg2': val2}, func(arg1=val1, arg2=val2)
        )

    def test_docstring_preserved(self):
        @rail.partial
        def func1(arg1, arg2):
            """Docstring for func"""
            return arg1, arg2
        self.assertEqual('Docstring for func', func1.__doc__)
        func2 = func1(unittest.mock.Mock())
        self.assertEqual('Docstring for func', func2.__doc__)


class TestCompose(unittest.TestCase):
    def test_compose_with_no_funcs(self):
        func = rail.compose()
        value = unittest.mock.Mock()
        self.assertEqual(value, func(value))

    def test_compose_with_no_exception(self):
        expected_value = unittest.mock.Mock()
        func = rail.compose(
            lambda value: expected_value
        )
        self.assertEqual(expected_value, func(unittest.mock.Mock()))

    def test_compose_with_exception(self):
        with self.assertRaises(ValueError) as context:
            func = rail.compose(
                lambda value: rail.RAISE(ValueError('exception'))
            )
            func(unittest.mock.Mock())
        self.assertEqual('exception', str(context.exception))

    def test_compose_with_multiple_funcs(self):
        return_value1 = unittest.mock.Mock()
        return_value2 = unittest.mock.Mock()
        return_value3 = unittest.mock.Mock()
        func1 = unittest.mock.Mock(return_value=return_value1)
        func2 = unittest.mock.Mock(return_value=return_value2)
        func3 = unittest.mock.Mock(return_value=return_value3)
        func = rail.compose(
            func1,
            func2,
            func3
        )
        value = unittest.mock.Mock()
        self.assertEqual(return_value3, func(value))
        func1.assert_called_once_with(value)
        func2.assert_called_once_with(return_value1)
        func3.assert_called_once_with(return_value2)


class TestPipe(unittest.TestCase):
    def test_pipe(self):
        val1 = unittest.mock.Mock()
        val2 = unittest.mock.Mock()
        val3 = unittest.mock.Mock()
        self.assertEqual(
            (val1, val2, val3),
            rail.pipe(
                (val1,),
                lambda val: val + (val2,),
                lambda val: val + (val3,)
            )
        )

    def test_use_pipe_to_create_scope(self):
        val1 = unittest.mock.Mock()
        val2 = unittest.mock.Mock()
        val3 = unittest.mock.Mock()
        self.assertEqual(
            (val1, val2, val3),
            rail.pipe(
                (val1,),
                lambda arg1: rail.pipe(
                    (val2,),
                    lambda arg2: arg1 + arg2,
                    lambda arg: arg + (val3,)
                )
            )
        )


class TestTee(unittest.TestCase):
    def test_with_multiple_funcs(self):
        input = unittest.mock.Mock()
        func1 = unittest.mock.Mock(return_value=unittest.mock.Mock())
        func2 = unittest.mock.Mock(return_value=unittest.mock.Mock())
        func3 = unittest.mock.Mock()
        self.assertEqual(
            input,
            rail.pipe(input, rail.tee(func1, func2, func3))
        )
        func1.assert_called_once_with(input)
        func2.assert_called_once_with(func1.return_value)
        func3.assert_called_once_with(func2.return_value)


class TestLt(unittest.TestCase):
    def test_pipe_returns_true(self):
        self.assertTrue(rail.pipe(5, rail.lt(7)))

    def test_pipe_returns_false(self):
        self.assertFalse(rail.pipe(8, rail.lt(1)))


class TestLe(unittest.TestCase):
    def test_pipe_returns_true_for_different_values(self):
        self.assertTrue(rail.pipe(5, rail.le(7)))

    def test_pipe_returns_true_for_equal_values(self):
        self.assertTrue(rail.pipe(5, rail.le(5)))

    def test_pipe_returns_false(self):
        self.assertFalse(rail.pipe(8, rail.le(1)))


class TestEq(unittest.TestCase):
    def test_pipe_returns_true(self):
        value = unittest.mock.Mock()
        self.assertTrue(rail.pipe(value, rail.eq(value)))

    def test_pipe_returns_false(self):
        value1 = unittest.mock.Mock()
        value2 = unittest.mock.Mock()
        self.assertFalse(rail.pipe(value1, rail.eq(value2)))


class TestNe(unittest.TestCase):
    def test_pipe_returns_true(self):
        value1 = unittest.mock.Mock()
        value2 = unittest.mock.Mock()
        self.assertTrue(rail.pipe(value1, rail.ne(value2)))

    def test_pipe_returns_false(self):
        value = unittest.mock.Mock()
        self.assertFalse(rail.pipe(value, rail.ne(value)))


class TestGt(unittest.TestCase):
    def test_pipe_returns_true(self):
        self.assertTrue(rail.pipe(4, rail.gt(0)))

    def test_pipe_returns_false(self):
        self.assertFalse(rail.pipe(13, rail.gt(15)))


class TestGe(unittest.TestCase):
    def test_pipe_returns_true_for_different_values(self):
        self.assertTrue(rail.pipe(6, rail.ge(2)))

    def test_pipe_returns_true_for_equal_values(self):
        self.assertTrue(rail.pipe(4, rail.ge(4)))

    def test_pipe_returns_false(self):
        self.assertFalse(rail.pipe(6, rail.ge(9)))


class TestTrack(unittest.TestCase):
    def test_compose_with_existing_func(self):
        return_value1 = unittest.mock.Mock()
        return_value2 = unittest.mock.Mock()
        return_value3 = unittest.mock.Mock()
        func1 = unittest.mock.Mock(return_value=return_value1)
        func2 = unittest.mock.Mock(return_value=return_value2)
        func3 = unittest.mock.Mock(return_value=return_value3)
        func = rail.Track().compose(
            func1
        ).compose(
            func2,
            func3
        )
        value = unittest.mock.Mock()
        self.assertEqual(return_value3, func(value))
        func1.assert_called_once_with(value)
        func2.assert_called_once_with(return_value1)
        func3.assert_called_once_with(return_value2)

    def test_tee_called_consecutively(self):
        func1 = unittest.mock.Mock()
        func2 = unittest.mock.Mock()
        func = rail.Track().tee(
            func1
        ).tee(
            func2
        )
        value = unittest.mock.Mock()
        self.assertEqual(value, func(value))
        func1.assert_called_once_with(value)
        func2.assert_called_once_with(value)

    def test_fold_with_no_exception(self):
        expected_value = unittest.mock.Mock()
        func = rail.Track().compose(
            lambda value: unittest.mock.Mock()
        ).fold(
            lambda value: expected_value,
            lambda exception: self.fail()
        )
        self.assertEqual(expected_value, func(unittest.mock.Mock()))

    def test_fold_with_exception(self):
        expected_exception = KeyError('key')
        actual_exception = rail.pipe(
            unittest.mock.Mock(),
            rail.Track().compose(
                lambda _: rail.RAISE(expected_exception)
            ).fold(
                lambda _: self.fail(),
                rail.identity
            )
        )
        self.assertEqual(expected_exception, actual_exception)

    def test_fold_traceback_with_exception(self):
        exception = KeyError('key')
        func = rail.Track().compose(
            lambda _: rail.RAISE(exception)
        )
        try:
            func(unittest.mock.Mock())
        except KeyError:
            expected_exc_info = sys.exc_info()
        try:
            rail.pipe(
                unittest.mock.Mock(),
                func.fold(
                    lambda _: self.fail(),
                    rail.RAISE
                )
            )
        except KeyError:
            actual_exc_info = sys.exc_info()
        self.assertEqual(expected_exc_info[0], actual_exc_info[0])
        self.assertEqual(expected_exc_info[1], actual_exc_info[1])
        expected_tb = traceback.format_tb(expected_exc_info[2])
        actual_tb = traceback.format_tb(actual_exc_info[2])
        self.assertEqual(expected_tb, actual_tb[-len(expected_tb):])

    def test_handle_with_multiple_funcs(self):
        expected_exception = ValueError('value')
        func = rail.Track().compose(
            lambda value: rail.RAISE(ValueError('value'))
        ).handle(
            lambda exception: unittest.mock.Mock(),
            lambda exception: expected_exception
        )
        self.assertEqual(expected_exception, func(unittest.mock.Mock()))

    def test_handle_with_no_exception(self):
        expected_value = unittest.mock.Mock()
        func = rail.Track().compose(
            lambda value: expected_value
        ).handle(
            lambda exception: self.fail()
        )
        self.assertEqual(expected_value, func(unittest.mock.Mock()))

    def test_handle_with_exception(self):
        expected_exception = KeyError('key')
        actual_exception = rail.pipe(
            unittest.mock.Mock(),
            rail.Track().compose(
                lambda _: rail.RAISE(expected_exception)
            ).handle(
                rail.identity
            )
        )
        self.assertEqual(expected_exception, actual_exception)

    def test_handle_traceback_with_exception(self):
        exception = KeyError('key')
        func = rail.Track().compose(
            lambda _: rail.RAISE(exception)
        )
        try:
            func(unittest.mock.Mock())
        except KeyError:
            expected_exc_info = sys.exc_info()
        try:
            rail.pipe(
                unittest.mock.Mock(),
                func.handle(
                    rail.RAISE
                )
            )
        except KeyError:
            actual_exc_info = sys.exc_info()
        self.assertEqual(expected_exc_info[0], actual_exc_info[0])
        self.assertEqual(expected_exc_info[1], actual_exc_info[1])
        expected_tb = traceback.format_tb(expected_exc_info[2])
        actual_tb = traceback.format_tb(actual_exc_info[2])
        self.assertEqual(expected_tb, actual_tb[-len(expected_tb):])


if __name__ == '__main__':
    unittest.main()

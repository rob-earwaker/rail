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
    def test_raises_error(self):
        with self.assertRaises(ValueError) as context:
            rail.RAISE(ValueError('error'))
        self.assertEqual('error', str(context.exception))

    def test_preserves_traceback_when_reraising_without_exception(self):
        def func(error):
            raise error
        try:
            try:
                func(ValueError('error'))
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
        def func(error):
            raise error
        try:
            try:
                func(ValueError('error'))
            except ValueError as error:
                expected_exc_info = sys.exc_info()
                rail.RAISE(error)
        except ValueError:
            actual_exc_info = sys.exc_info()
        self.assertEqual(expected_exc_info[0], actual_exc_info[0])
        self.assertEqual(expected_exc_info[1], actual_exc_info[1])
        expected_tb = traceback.format_tb(expected_exc_info[2])
        actual_tb = traceback.format_tb(actual_exc_info[2])
        self.assertEqual(expected_tb, actual_tb[-len(expected_tb):])


class TestIgnore(unittest.TestCase):
    def test_ignores_input_value(self):
        self.assertIsNone(rail.ignore(unittest.mock.Mock()))


class TestTry(unittest.TestCase):
    def test_no_error_raised(self):
        input = unittest.mock.Mock()
        expected_value = unittest.mock.Mock()
        func = unittest.mock.Mock(return_value=expected_value)
        handle = unittest.mock.Mock()
        self.assertEqual(expected_value, rail.TRY(input, func, handle))
        func.assert_called_once_with(input)
        handle.assert_not_called()

    def test_error_raised(self):
        input = unittest.mock.Mock()
        error = rail.Error()
        func = unittest.mock.Mock(side_effect=lambda _: rail.RAISE(error))
        output = unittest.mock.Mock()
        handle = unittest.mock.Mock(return_value=output)
        self.assertEqual(output, rail.TRY(input, func, handle))
        func.assert_called_once_with(input)
        handle.assert_called_once_with(error)


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


class TestCompose(unittest.TestCase):
    def test_compose_with_no_funcs(self):
        func = rail.compose()
        value = unittest.mock.Mock()
        self.assertEqual(value, func(value))

    def test_compose_with_no_error(self):
        expected_value = unittest.mock.Mock()
        func = rail.compose(
            lambda value: expected_value
        )
        self.assertEqual(expected_value, func(unittest.mock.Mock()))

    def test_compose_with_error(self):
        with self.assertRaises(rail.Error) as context:
            func = rail.compose(
                lambda value: rail.RAISE(rail.Error('error'))
            )
            func(unittest.mock.Mock())
        self.assertEqual('error', str(context.exception))

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

    def test_fold_with_no_error(self):
        expected_value = unittest.mock.Mock()
        func = rail.Track().compose(
            lambda value: unittest.mock.Mock()
        ).fold(
            lambda value: expected_value,
            lambda error: self.fail()
        )
        self.assertEqual(expected_value, func(unittest.mock.Mock()))

    def test_fold_with_error(self):
        expected_error = rail.Error()
        func = rail.Track().compose(
            lambda value: rail.RAISE(expected_error)
        ).fold(
            lambda value: self.fail(),
            rail.identity
        )
        self.assertEqual(expected_error, func(unittest.mock.Mock()))

    def test_fold_with_standard_exception(self):
        expected_exception = KeyError('key')
        with self.assertRaises(KeyError) as context:
            rail.pipe(
                unittest.mock.Mock(),
                rail.Track().compose(
                    lambda _: rail.RAISE(expected_exception)
                ).fold(
                    lambda _: self.fail(),
                    lambda _: self.fail()
                )
            )
        self.assertEqual(expected_exception, context.exception)

    def test_fold_traceback_with_standard_exception(self):
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
                    lambda _: self.fail()
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
        expected_error = rail.Error()
        func = rail.Track().compose(
            lambda value: rail.RAISE(rail.Error())
        ).handle(
            lambda error: unittest.mock.Mock(),
            lambda error: expected_error
        )
        self.assertEqual(expected_error, func(unittest.mock.Mock()))

    def test_handle_with_no_error(self):
        expected_value = unittest.mock.Mock()
        func = rail.Track().compose(
            lambda value: expected_value
        ).handle(
            lambda error: self.fail()
        )
        self.assertEqual(expected_value, func(unittest.mock.Mock()))

    def test_handle_with_error(self):
        expected_error = rail.Error()
        func = rail.Track().compose(
            lambda value: rail.RAISE(expected_error)
        ).handle(
            lambda error: error
        )
        self.assertEqual(expected_error, func(unittest.mock.Mock()))

    def test_handle_with_standard_exception(self):
        expected_exception = KeyError('key')
        with self.assertRaises(KeyError) as context:
            rail.pipe(
                unittest.mock.Mock(),
                rail.Track().compose(
                    lambda _: rail.RAISE(expected_exception)
                ).handle(
                    lambda _: self.fail()
                )
            )
        self.assertEqual(expected_exception, context.exception)

    def test_handle_traceback_with_standard_exception(self):
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
                    lambda _: self.fail()
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

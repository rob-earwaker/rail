import mock
import unittest

import rail


class TestIdentity(unittest.TestCase):
    def test_returns_input_value(self):
        value = mock.Mock()
        self.assertEqual(value, rail.identity(value))


class TestRaiseError(unittest.TestCase):
    def test_raises_error(self):
        with self.assertRaises(ValueError) as context:
            rail.raise_error(ValueError('error'))
        self.assertEqual('error', str(context.exception))


class TestIgnore(unittest.TestCase):
    def test_ignores_input_value(self):
        self.assertIsNone(rail.ignore(mock.Mock()))


class TestMatch(unittest.TestCase):
    def test_no_match_statements_provided(self):
        value = mock.Mock()
        with self.assertRaises(rail.UnmatchedValueError) as context:
            rail.match()(value)
        self.assertEqual(value, context.exception.value)

    def test_value_unmatched_by_all_match_statements(self):
        value = mock.Mock()
        with self.assertRaises(rail.UnmatchedValueError) as context:
            match = rail.match(
                (lambda _: False, lambda _: mock.Mock()),
                (lambda _: False, lambda _: mock.Mock()),
                (lambda _: False, lambda _: mock.Mock())
            )
            match(value)
        self.assertEqual(value, context.exception.value)

    def test_value_matches_single_match_statement(self):
        expected_value = mock.Mock()
        match = rail.match(
            (lambda _: False, lambda _: mock.Mock()),
            (lambda _: True, lambda _: expected_value),
            (lambda _: False, lambda _: mock.Mock())
        )
        self.assertEqual(expected_value, match(mock.Mock()))

    def test_value_matches_multiple_match_statements(self):
        expected_value = mock.Mock()
        match = rail.match(
            (lambda _: False, lambda _: mock.Mock()),
            (lambda _: True, lambda _: expected_value),
            (lambda _: True, lambda _: mock.Mock())
        )
        self.assertEqual(expected_value, match(mock.Mock()))


class TestMatchType(unittest.TestCase):
    def test_no_match_statements_provided(self):
        value = mock.Mock()
        with self.assertRaises(rail.UnmatchedValueError) as context:
            rail.match_type()(value)
        self.assertEqual(value, context.exception.value)

    def test_value_unmatched_by_all_match_statements(self):
        value = mock.Mock()
        with self.assertRaises(rail.UnmatchedValueError) as context:
            match = rail.match_type(
                (str, lambda _: mock.Mock()),
                (float, lambda _: mock.Mock()),
                (Exception, lambda _: mock.Mock())
            )
            match(value)
        self.assertEqual(value, context.exception.value)

    def test_value_matches_single_match_statement(self):
        expected_value = mock.Mock()
        match = rail.match_type(
            (int, lambda _: mock.Mock()),
            (mock.Mock, lambda _: expected_value),
            (dict, lambda _: mock.Mock())
        )
        self.assertEqual(expected_value, match(mock.Mock()))

    def test_value_matches_multiple_match_statements(self):
        expected_value = mock.Mock()
        match = rail.match_type(
            (bool, lambda _: mock.Mock()),
            (mock.Mock, lambda _: expected_value),
            (mock.Mock, lambda _: mock.Mock())
        )
        self.assertEqual(expected_value, match(mock.Mock()))

    def test_value_subclass_of_match_type(self):
        expected_value = mock.Mock()
        match = rail.match_type(
            (bool, lambda _: mock.Mock()),
            (object, lambda _: expected_value),
            (mock.Mock, lambda _: mock.Mock())
        )
        self.assertEqual(expected_value, match(mock.Mock()))


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
        value = mock.Mock()
        self.assertEqual(value, func(value))

    def test_func_with_multiple_args(self):
        @rail.partial
        def func(arg1, arg2, arg3):
            return arg1, arg2, arg3
        val1 = mock.Mock()
        val2 = mock.Mock()
        val3 = mock.Mock()
        self.assertEqual((val1, val2, val3), func(val1, val2, val3))
        self.assertEqual((val1, val2, val3), func(val1)(val2, val3))
        self.assertEqual((val1, val2, val3), func(val1, val2)(val3))
        self.assertEqual((val1, val2, val3), func(val1)(val2)(val3))

    def test_func_with_arguments_applied_out_of_order(self):
        @rail.partial
        def func(arg1, arg2, arg3):
            return arg1, arg2, arg3
        val1 = mock.Mock()
        val2 = mock.Mock()
        val3 = mock.Mock()
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
        val1 = mock.Mock()
        val2 = mock.Mock()
        val3 = mock.Mock()
        val4 = mock.Mock()
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
        val1 = mock.Mock()
        val2 = mock.Mock()
        self.assertEqual(('val1', 'val2'), func())
        self.assertEqual((val1, 'val2'), func(val1))
        self.assertEqual(('val1', val2), func(arg2=val2))
        self.assertEqual((val1, val2), func(val1, val2))

    def test_func_with_argument_list(self):
        @rail.partial
        def func(arg1, arg2, *args):
            return (arg1, arg2) + args
        val1 = mock.Mock()
        val2 = mock.Mock()
        val3 = mock.Mock()
        val4 = mock.Mock()
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
        val1 = mock.Mock()
        val2 = mock.Mock()
        self.assertEqual((), func())
        self.assertEqual((val1,), func(val1))
        self.assertEqual((val1, val2), func(val1, val2))

    def test_func_with_keyword_arguments(self):
        @rail.partial
        def func(arg1, arg2, **kwargs):
            return (arg1, arg2) + ((kwargs,) if kwargs else ())
        val1 = mock.Mock()
        val2 = mock.Mock()
        val3 = mock.Mock()
        val4 = mock.Mock()
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
        val1 = mock.Mock()
        val2 = mock.Mock()
        self.assertEqual({}, func())
        self.assertEqual({'arg1': val1}, func(arg1=val1))
        self.assertEqual(
            {'arg1': val1, 'arg2': val2}, func(arg1=val1, arg2=val2)
        )


class TestCompose(unittest.TestCase):
    def test_compose_with_no_funcs(self):
        func = rail.compose()
        value = mock.Mock()
        self.assertEqual(value, func(value))

    def test_compose_with_no_error(self):
        expected_value = mock.Mock()
        func = rail.compose(
            lambda value: expected_value
        )
        self.assertEqual(expected_value, func(mock.Mock()))

    def test_compose_with_error(self):
        with self.assertRaises(rail.Error) as context:
            func = rail.compose(
                lambda value: rail.raise_error(rail.Error('error'))
            )
            func(mock.Mock())
        self.assertEqual('error', str(context.exception))

    def test_compose_with_multiple_funcs(self):
        return_value1 = mock.Mock()
        return_value2 = mock.Mock()
        return_value3 = mock.Mock()
        func1 = mock.Mock(return_value=return_value1)
        func2 = mock.Mock(return_value=return_value2)
        func3 = mock.Mock(return_value=return_value3)
        func = rail.compose(
            func1,
            func2,
            func3
        )
        value = mock.Mock()
        self.assertEqual(return_value3, func(value))
        func1.assert_called_once_with(value)
        func2.assert_called_once_with(return_value1)
        func3.assert_called_once_with(return_value2)


class TestTrack(unittest.TestCase):
    def test_new(self):
        func = rail.Track.new()
        value = mock.Mock()
        self.assertEqual(value, func(value))

    def test_compose_with_existing_func(self):
        return_value1 = mock.Mock()
        return_value2 = mock.Mock()
        return_value3 = mock.Mock()
        func1 = mock.Mock(return_value=return_value1)
        func2 = mock.Mock(return_value=return_value2)
        func3 = mock.Mock(return_value=return_value3)
        func = rail.Track.new().compose(
            func1
        ).compose(
            func2,
            func3
        )
        value = mock.Mock()
        self.assertEqual(return_value3, func(value))
        func1.assert_called_once_with(value)
        func2.assert_called_once_with(return_value1)
        func3.assert_called_once_with(return_value2)

    def test_tee_with_multiple_funcs(self):
        return_value1 = mock.Mock()
        return_value2 = mock.Mock()
        func1 = mock.Mock(return_value=return_value1)
        func2 = mock.Mock(return_value=return_value2)
        func3 = mock.Mock()
        func = rail.Track.new().tee(
            func1,
            func2,
            func3
        )
        value = mock.Mock()
        self.assertEqual(value, func(value))
        func1.assert_called_once_with(value)
        func2.assert_called_once_with(return_value1)
        func3.assert_called_once_with(return_value2)

    def test_tee_called_consecutively(self):
        func1 = mock.Mock()
        func2 = mock.Mock()
        func = rail.Track.new().tee(
            func1
        ).tee(
            func2
        )
        value = mock.Mock()
        self.assertEqual(value, func(value))
        func1.assert_called_once_with(value)
        func2.assert_called_once_with(value)

    def test_tee_with_error(self):
        expected_error = rail.Error('error')
        func = rail.Track.new().tee(
            lambda _: rail.raise_error(expected_error)
        ).fold(
            lambda value: self.fail(),
            rail.identity
        )
        self.assertEqual(expected_error, func(mock.Mock()))

    def test_fold_with_no_error(self):
        expected_value = mock.Mock()
        func = rail.Track.new().compose(
            lambda value: mock.Mock()
        ).fold(
            lambda value: expected_value,
            lambda error: self.fail()
        )
        self.assertEqual(expected_value, func(mock.Mock()))

    def test_fold_with_error(self):
        expected_error = rail.Error()
        func = rail.Track.new().compose(
            lambda value: rail.raise_error(expected_error)
        ).fold(
            lambda value: self.fail(),
            rail.identity
        )
        self.assertEqual(expected_error, func(mock.Mock()))


if __name__ == '__main__':
    unittest.main()

import mock
import unittest

import rail


class TestIdentity(unittest.TestCase):
    def test_returns_input_value(self):
        value = mock.Mock()
        self.assertEqual(value, rail.identity(value))


class TestRaiseException(unittest.TestCase):
    def test_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            rail.raise_exception(ValueError('error'))
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


class TestCompose(unittest.TestCase):
    def test_compose_with_no_functions(self):
        function = rail.compose()
        value = mock.Mock()
        self.assertEqual(value, function(value))

    def test_compose_with_no_error(self):
        expected_value = mock.Mock()
        function = rail.compose(
            lambda value: expected_value
        )
        self.assertEqual(expected_value, function(mock.Mock()))

    def test_compose_with_error(self):
        with self.assertRaises(rail.Error) as context:
            function = rail.compose(
                lambda value: rail.raise_exception(rail.Error('error'))
            )
            function(mock.Mock())
        self.assertEqual('error', str(context.exception))

    def test_compose_with_multiple_functions(self):
        return_value1 = mock.Mock()
        return_value2 = mock.Mock()
        return_value3 = mock.Mock()
        function1 = mock.Mock(return_value=return_value1)
        function2 = mock.Mock(return_value=return_value2)
        function3 = mock.Mock(return_value=return_value3)
        function = rail.compose(
            function1,
            function2,
            function3
        )
        value = mock.Mock()
        self.assertEqual(return_value3, function(value))
        function1.assert_called_once_with(value)
        function2.assert_called_once_with(return_value1)
        function3.assert_called_once_with(return_value2)


class TestRail(unittest.TestCase):
    def test_new_with_no_function(self):
        value = mock.Mock()
        function = rail.Rail.new()
        self.assertEqual(value, function(value))

    def test_new_with_function(self):
        expected_value = mock.Mock()
        function = rail.Rail.new(
            lambda value: expected_value
        )
        self.assertEqual(expected_value, function(mock.Mock()))

    def test_compose_with_existing_function(self):
        return_value1 = mock.Mock()
        return_value2 = mock.Mock()
        return_value3 = mock.Mock()
        function1 = mock.Mock(return_value=return_value1)
        function2 = mock.Mock(return_value=return_value2)
        function3 = mock.Mock(return_value=return_value3)
        function = rail.Rail.new(
            function1
        ).compose(
            function2,
            function3
        )
        value = mock.Mock()
        self.assertEqual(return_value3, function(value))
        function1.assert_called_once_with(value)
        function2.assert_called_once_with(return_value1)
        function3.assert_called_once_with(return_value2)

    def test_tee_with_multiple_functions(self):
        return_value1 = mock.Mock()
        return_value2 = mock.Mock()
        return_value3 = mock.Mock()
        function1 = mock.Mock(return_value=return_value1)
        function2 = mock.Mock(return_value=return_value2)
        function3 = mock.Mock(return_value=return_value3)
        function = rail.Rail.new().tee(
            function1,
            function2,
            function3
        )
        value = mock.Mock()
        self.assertEqual(value, function(value))
        function1.assert_called_once_with(value)
        function2.assert_called_once_with(return_value1)
        function3.assert_called_once_with(return_value2)

    def test_fold_with_no_error(self):
        expected_value = mock.Mock()
        function = rail.Rail.new().compose(
            lambda value: mock.Mock()
        ).fold(
            lambda value: expected_value,
            lambda error: self.fail()
        )
        self.assertEqual(expected_value, function(mock.Mock()))

    def test_fold_with_error(self):
        expected_error = rail.Error()
        function = rail.Rail.new().compose(
            lambda value: rail.raise_exception(expected_error)
        ).fold(
            lambda value: self.fail(),
            rail.identity
        )
        self.assertEqual(expected_error, function(mock.Mock()))


if __name__ == '__main__':
    unittest.main()

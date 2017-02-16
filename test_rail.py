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
        expected_result = mock.Mock()
        match = rail.match(
            (lambda _: False, lambda _: mock.Mock()),
            (lambda _: True, lambda _: expected_result),
            (lambda _: False, lambda _: mock.Mock())
        )
        self.assertEqual(expected_result, match(mock.Mock()))

    def test_value_matches_multiple_match_statements(self):
        expected_result = mock.Mock()
        match = rail.match(
            (lambda _: False, lambda _: mock.Mock()),
            (lambda _: True, lambda _: expected_result),
            (lambda _: True, lambda _: mock.Mock())
        )
        self.assertEqual(expected_result, match(mock.Mock()))


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
        expected_result = mock.Mock()
        match = rail.match_type(
            (int, lambda _: mock.Mock()),
            (mock.Mock, lambda _: expected_result),
            (dict, lambda _: mock.Mock())
        )
        self.assertEqual(expected_result, match(mock.Mock()))

    def test_value_matches_multiple_match_statements(self):
        expected_result = mock.Mock()
        match = rail.match_type(
            (bool, lambda _: mock.Mock()),
            (mock.Mock, lambda _: expected_result),
            (mock.Mock, lambda _: mock.Mock())
        )
        self.assertEqual(expected_result, match(mock.Mock()))

    def test_value_subclass_of_match_type(self):
        expected_result = mock.Mock()
        match = rail.match_type(
            (bool, lambda _: mock.Mock()),
            (object, lambda _: expected_result),
            (mock.Mock, lambda _: mock.Mock())
        )
        self.assertEqual(expected_result, match(mock.Mock()))


if __name__ == '__main__':
    unittest.main()

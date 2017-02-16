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
                (lambda value: False, lambda value: mock.Mock()),
                (lambda value: False, lambda value: mock.Mock()),
                (lambda value: False, lambda value: mock.Mock())
            )
            match(value)
        self.assertEqual(value, context.exception.value)

    def test_value_matches_single_match_statement(self):
        expected = mock.Mock()
        match = rail.match(
            (lambda value: False, lambda value: mock.Mock()),
            (lambda value: True, lambda value: expected),
            (lambda value: False, lambda value: mock.Mock())
        )
        self.assertEqual(expected, match(mock.Mock()))

    def test_value_matches_multiple_match_statements(self):
        expected = mock.Mock()
        match = rail.match(
            (lambda value: False, lambda value: mock.Mock()),
            (lambda value: True, lambda value: expected),
            (lambda value: True, lambda value: mock.Mock())
        )
        self.assertEqual(expected, match(mock.Mock()))


if __name__ == '__main__':
    unittest.main()

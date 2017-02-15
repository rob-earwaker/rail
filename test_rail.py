import mock
import unittest

import rail


class TestIdentity(unittest.TestCase):
    def test_returns_input_value(self):
        value = mock.Mock()
        self.assertEqual(value, rail.identity(value))


class TestRaiseException(unittest.TestCase):
    def test_raises_exception(self):
        with self.assertRaisesRegex(ValueError, '^failure$'):
            rail.raise_exception(ValueError('failure'))


if __name__ == '__main__':
    unittest.main()

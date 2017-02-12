import mock
import unittest

import rail


class TestResult(unittest.TestCase):
    def test_fold_with_success_input(self):
        value = rail.Result.success('success').fold(
            lambda success: success,
            lambda failure: 'failure'
        )
        self.assertEqual('success', value)

    def test_fold_with_failure_input(self):
        value = rail.Result.failure('failure').fold(
            lambda success: 'success',
            lambda failure: failure
        )
        self.assertEqual('failure', value)

    def test_map_either_with_success_input(self):
        rail.Result.success(
            'mock'
        ).map_either(
            lambda success: 'success',
            lambda failure: 'failure'
        ).fold(
            lambda success: self.assertEqual('success', success),
            lambda failure: self.fail()
        )

    def test_map_either_with_failure_input(self):
        rail.Result.failure(
            'mock'
        ).map_either(
            lambda success: 'success',
            lambda failure: 'failure'
        ).fold(
            lambda success: self.fail(),
            lambda failure: self.assertEqual('failure', failure)
        )

    def test_map_success_with_success_input(self):
        rail.Result.success(
            'mock'
        ).map_success(
            lambda success: 'success'
        ).fold(
            lambda success: self.assertEqual('success', success),
            lambda failure: self.fail()
        )

    def test_map_success_with_failure_input(self):
        rail.Result.failure(
            'failure'
        ).map_success(
            lambda success: 'success'
        ).fold(
            lambda success: self.fail(),
            lambda failure: self.assertEqual('failure', failure)
        )

    def test_switch_success_with_success_input_and_success_result(self):
        rail.Result.success(
            'mock'
        ).switch_success(
            lambda success: rail.Result.success('success')
        ).fold(
            lambda success: self.assertEqual('success', success),
            lambda failure: self.fail()
        )

    def test_switch_success_with_success_input_and_failure_result(self):
        rail.Result.success(
            'success'
        ).switch_success(
            lambda success: rail.Result.failure('failure')
        ).fold(
            lambda success: self.fail(),
            lambda failure: self.assertEqual('failure', failure)
        )

    def test_switch_success_with_failure_input_and_success_result(self):
        rail.Result.failure(
            'failure'
        ).switch_success(
            lambda success: rail.Result.success('success')
        ).fold(
            lambda success: self.fail(),
            lambda failure: self.assertEqual('failure', failure)
        )

    def test_switch_success_with_failure_input_and_failure_result(self):
        rail.Result.failure(
            'failure'
        ).switch_success(
            lambda success: rail.Result.failure('mock')
        ).fold(
            lambda success: self.fail(),
            lambda failure: self.assertEqual('failure', failure)
        )

    def test_switch_failure_with_success_input_and_success_result(self):
        rail.Result.success(
            'success'
        ).switch_failure(
            lambda failure: rail.Result.success('mock')
        ).fold(
            lambda success: self.assertEqual('success', success),
            lambda failure: self.fail()
        )

    def test_switch_failure_with_success_input_and_failure_result(self):
        rail.Result.success(
            'success'
        ).switch_failure(
            lambda failure: rail.Result.failure('failure')
        ).fold(
            lambda success: self.assertEqual('success', success),
            lambda failure: self.fail()
        )

    def test_switch_failure_with_failure_input_and_success_result(self):
        rail.Result.failure(
            'failure'
        ).switch_failure(
            lambda failure: rail.Result.success('success')
        ).fold(
            lambda success: self.assertEqual('success', success),
            lambda failure: self.fail()
        )

    def test_switch_failure_with_failure_input_and_failure_result(self):
        rail.Result.failure(
            'mock'
        ).switch_failure(
            lambda failure: rail.Result.failure('failure')
        ).fold(
            lambda success: self.fail(),
            lambda failure: self.assertEqual('failure', failure)
        )

    def test_tee_either_with_success_input(self):
        tee_success = mock.Mock()
        tee_failure = mock.Mock()
        rail.Result.success(
            'success'
        ).tee_either(
            lambda success: tee_success(success),
            lambda failure: tee_failure(failure)
        ).fold(
            lambda success: self.assertEqual('success', success),
            lambda failure: self.fail()
        )
        tee_success.assert_called_once_with('success')
        tee_failure.assert_not_called()

    def test_tee_either_with_failure_input(self):
        tee_success = mock.Mock()
        tee_failure = mock.Mock()
        rail.Result.failure(
            'failure'
        ).tee_either(
            lambda success: tee_success(success),
            lambda failure: tee_failure(failure)
        ).fold(
            lambda success: self.fail(),
            lambda failure: self.assertEqual('failure', failure)
        )
        tee_success.assert_not_called()
        tee_failure.assert_called_once_with('failure')

    def test_tee_success_with_success_input(self):
        tee_success = mock.Mock()
        rail.Result.success(
            'success'
        ).tee_success(
            lambda success: tee_success(success)
        ).fold(
            lambda success: self.assertEqual('success', success),
            lambda failure: self.fail()
        )
        tee_success.assert_called_once_with('success')

    def test_tee_success_with_failure_input(self):
        tee_success = mock.Mock()
        rail.Result.failure(
            'failure'
        ).tee_success(
            lambda success: tee_success(success)
        ).fold(
            lambda success: self.fail(),
            lambda failure: self.assertEqual('failure', failure)
        )
        tee_success.assert_not_called()

    def test_tee_failure_with_success_input(self):
        tee_failure = mock.Mock()
        rail.Result.success(
            'success'
        ).tee_failure(
            lambda failure: tee_failure(failure)
        ).fold(
            lambda success: self.assertEqual('success', success),
            lambda failure: self.fail()
        )
        tee_failure.assert_not_called()

    def test_tee_failure_with_failure_input(self):
        tee_failure = mock.Mock()
        rail.Result.failure(
            'failure'
        ).tee_failure(
            lambda failure: tee_failure(failure)
        ).fold(
            lambda success: self.fail(),
            lambda failure: self.assertEqual('failure', failure)
        )
        tee_failure.assert_called_once_with('failure')


if __name__ == '__main__':
    unittest.main()

class Result(object):
    def __init__(self, success, failure, is_success):
        self._success = success
        self._failure = failure
        self._is_success = is_success

    @classmethod
    def success(cls, success):
        return cls(success=success, failure=None, is_success=True)

    @classmethod
    def failure(cls, failure):
        return cls(success=None, failure=failure, is_success=False)

    def fold(self, fold_success, fold_failure):
        return (
            fold_success(self._success) if self._is_success
            else fold_failure(self._failure)
        )

    def map_either(self, map_success, map_failure):
        return self.fold(
            lambda success: Result.success(map_success(success)),
            lambda failure: Result.failure(map_failure(failure))
        )

    def map_success(self, map_success):
        return self.map_either(
            lambda success: map_success(success),
            lambda failure: failure
        )

    def map_failure(self, map_failure):
        return self.map_either(
            lambda success: success,
            lambda failure: map_failure(failure)
        )

    def switch_success(self, switch_success):
        return self.fold(
            lambda success: switch_success(success),
            lambda failure: Result.failure(failure)
        )

    def switch_failure(self, switch_failure):
        return self.fold(
            lambda success: Result.success(success),
            lambda failure: switch_failure(failure)
        )

    def tee_either(self, tee_success, tee_failure):
        self.fold(
            lambda success: tee_success(success),
            lambda failure: tee_failure(failure)
        )
        return self

    def tee_success(self, tee_success):
        return self.tee_either(
            lambda success: tee_success(success),
            lambda failure: None
        )

    def tee_failure(self, tee_failure):
        return self.tee_either(
            lambda success: None,
            lambda failure: tee_failure(failure)
        )

class UnsolvableModelError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class IncompleteResultsError(Exception):
    def __init__(self, message, results = None):
        super().__init__(message)
        self.message = message
        self.results = results

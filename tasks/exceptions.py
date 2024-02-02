class DuplicateTaskAssignmentException(Exception):
    pass


class UnassignableTaskSet(Exception):
    pass


class LowCriticalityJobWhileOverrun(Exception):
    pass


class HighCriticalityTaskFailureException(Exception):
    def __init__(self, job):
        super().__init__()
        self.job = job

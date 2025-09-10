import itertools

class IdGenerator:
    """Sinh ID tăng dần theo prefix: PROD-1, CUST-1, ..."""
    def __init__(self, prefix: str):
        self.prefix = prefix
        self._counter = itertools.count(1)

    def next(self) -> str:
        return f"{self.prefix}-{next(self._counter)}"

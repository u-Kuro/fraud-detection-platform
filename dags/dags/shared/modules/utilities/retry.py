import time
from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager

type Exceptions = type[BaseException] | tuple[type[BaseException], ...]

def retry(
    ignored_exceptions: Exceptions,
    attempts: int = 5,
    delay: float = 5,
) -> Iterator[AbstractContextManager[None]]:
    succeeded = False

    @contextmanager
    def attempt(is_last: bool):
        nonlocal succeeded
        try:
            yield
            succeeded = True
        except ignored_exceptions:
            if is_last: raise
            time.sleep(delay)

    for n in range(1, attempts + 1):
        yield attempt(n == attempts)
        if succeeded: return
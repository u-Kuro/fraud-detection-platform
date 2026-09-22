import threading
import time

class AlreadyProcessed(Exception): pass

class IdempotencyGuard:
    def __init__(self, store: "IdempotencyStore", key: str):
        self.store = store
        self.key   = key

    def __enter__(self) -> "IdempotencyGuard":
        with self.store.lock:
            expiration = self.store.completed.get(self.key)
            if expiration is None:
                self.store.completed[self.key] = time.monotonic() + self.store.ttl
            elif expiration >= time.monotonic():
                raise AlreadyProcessed()
        return self

    def __exit__(self, exception_type, *args) -> bool:
        if exception_type is AlreadyProcessed: return True
        if exception_type is None:
            with self.store.lock:
                self.store.completed.pop(self.key, None)
        return False

class IdempotencyStore:
    def __init__(
        self,
        ttl: float,
        cleanup_interval: float | None = None,
    ):
        self.completed: dict[str, float] = {}
        self.ttl = ttl
        self.cleanup_interval = (
            cleanup_interval if cleanup_interval is not None
            else max(ttl / 2, 1)
        )
        self.lock = threading.Lock()

        def cleanup_loop():
            while True:
                time.sleep(self.cleanup_interval)
                self.purge_expired()
        threading.Thread(
            target=cleanup_loop,
            daemon=True,
            name="idempotency-cleanup"
        ).start()

    def purge_expired(self) -> None:
        with self.lock:
            now = time.monotonic()
            expired = [key for key, expiration in self.completed.items() if expiration <= now]
            for key in expired:
                del self.completed[key]

    def guard(self, *parts: str) -> IdempotencyGuard:
        return IdempotencyGuard(self, ":".join(parts))

    def __len__(self) -> int:
        with self.lock:
            return len(self.completed)
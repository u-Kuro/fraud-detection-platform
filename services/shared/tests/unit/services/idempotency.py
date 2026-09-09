import threading
import time

import pytest

from services.shared.src.services.idempotency import IdempotencyStore, AlreadyProcessed

class TestAlreadyProcessed:
    def test_identity(self):
        assert issubclass(AlreadyProcessed, Exception)

    def test_raise(self):
        with pytest.raises(AlreadyProcessed):
            raise AlreadyProcessed()

class TestIdempotencyStore:
    @staticmethod
    @pytest.fixture
    def idempotency_store() -> IdempotencyStore:
        return IdempotencyStore(ttl=60)

    def test_usage(self, idempotency_store: IdempotencyStore):
        with idempotency_store.guard("a"):
            pass

    def test_success_for_distinct_keys(self, idempotency_store: IdempotencyStore):
        idempotency_store.completed["a"] = time.monotonic() + 60
        with idempotency_store.guard("b"):
            pass

    def test_failure_for_duplicate_keys(self, idempotency_store: IdempotencyStore):
        idempotency_store.completed["a"] = time.monotonic() + 60
        with pytest.raises(AlreadyProcessed):
            with idempotency_store.guard("a"):
                pass

    def test_key_removal_after_success(self, idempotency_store: IdempotencyStore):
        with idempotency_store.guard("a"):
            pass
        assert len(idempotency_store) == 0

    def test_key_persistence_after_failure(self, idempotency_store: IdempotencyStore):
        try:
            with idempotency_store.guard("a"):
                raise RuntimeError
        except RuntimeError:
            pass
        assert "a" in idempotency_store.completed

    def test_success_for_expired_key_reprocessing(self, idempotency_store: IdempotencyStore):
        idempotency_store.completed["a"] = time.monotonic() - 1
        with idempotency_store.guard("a"):
            pass

    def test_purge_removal_for_expired_keys(self, idempotency_store: IdempotencyStore):
        idempotency_store.completed["stale"] = time.monotonic() - 1
        idempotency_store.completed["fresh"] = time.monotonic() + 60

        idempotency_store.purge_expired()

        assert len(idempotency_store) == 1
        assert "stale" not in idempotency_store.completed
        assert "fresh" in idempotency_store.completed

    def test_items_size(self, idempotency_store: IdempotencyStore):
        assert len(idempotency_store) == 0

        idempotency_store.completed["a"] = time.monotonic() + 60
        idempotency_store.completed["b"] = time.monotonic() + 60

        assert len(idempotency_store) == 2

    def test_only_one_key_is_accepted_in_concurrent_setting(self, idempotency_store: IdempotencyStore):
        concurrent_items = 10
        barrier = threading.Barrier(concurrent_items)

        inside = []
        def attempt():
            barrier.wait()
            try:
                with idempotency_store.guard("shared"):
                    time.sleep(1)
                    inside.append(1)
            except AlreadyProcessed:
                pass

        threads = [threading.Thread(target=attempt) for _ in range(concurrent_items)]
        for thread in threads: thread.start()
        for thread in threads: thread.join()

        assert len(inside) < concurrent_items
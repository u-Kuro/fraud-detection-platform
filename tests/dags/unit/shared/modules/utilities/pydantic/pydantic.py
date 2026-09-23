import pytest
from pydantic import StrictStr, ValidationError

from dags.shared.modules.utilities.pydantic.pydantic import validated_lru_cache

class TestValidatedLRUCache:
    def test_lru_cache(self):
        function_calls = 0

        @validated_lru_cache
        def function(value: StrictStr) -> StrictStr:
            nonlocal function_calls
            function_calls += 1
            return value

        assert function("value") == "value"
        assert function_calls == 1
        assert function("value") == "value"
        assert function_calls == 1

    def test_arguments_validation(self):
        @validated_lru_cache
        def function(value: StrictStr) -> StrictStr:
            return value

        assert function("value") == "value"

        with pytest.raises(ValidationError):
            function(1)

    def test_return_validation(self):
        @validated_lru_cache
        def function() -> StrictStr:
            return 1

        with pytest.raises(ValidationError):
            function()
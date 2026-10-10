import pytest
from pydantic import StrictStr, ValidationError

from shared.modules.utilities.pydantic.pydantic import validated_cache

class TestValidatedCache:
    def test_cache(self):
        function_calls = 0

        @validated_cache
        def function(value: StrictStr) -> StrictStr:
            nonlocal function_calls
            function_calls += 1
            return value

        assert function("value") == "value"
        assert function_calls == 1
        assert function("value") == "value"
        assert function_calls == 1

    def test_arguments_validation(self):
        @validated_cache
        def function(value: StrictStr) -> StrictStr:
            return value

        assert function("value") == "value"

        with pytest.raises(ValidationError):
            function(1)

    def test_return_validation(self):
        @validated_cache
        def function() -> StrictStr:
            return 1

        with pytest.raises(ValidationError):
            function()
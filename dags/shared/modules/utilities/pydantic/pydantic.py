from functools import lru_cache
from typing import Callable, cast

from pydantic import validate_call

def validated_lru_cache[T](
    function: Callable[..., T],
) -> Callable[..., T]:
    validated = validate_call(validate_return=True)(function)
    return cast(Callable[..., T], lru_cache(maxsize=None)(validated))

# class NamedCachedProperty[T](cached_property[T]):
#     def __init__(self, function: Callable[..., T]):
#         super().__init__(function)
#         self.__name__ = function.__name__
#
# def validated_cached_property[T](
#     function: Callable[..., T],
# ) -> NamedCachedProperty[T]:
#     validated = validate_call(validate_return=True)(function)
#     return NamedCachedProperty(validated)
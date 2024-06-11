"""Test persist-cache."""
import os
import random
import shutil
import time
from typing import AsyncGenerator, Callable, Generator, Union

import persist_cache


def _time_consuming_function(
    *args,
    str_: str = None,
    int_: int = None,
    list_: list[int] = None,
    dict_: dict[str, int] = None,
    tuple_: tuple[int, str] = None,
    set_: set[int] = None,
    frozenset_: frozenset[int] = None,
    bytes_: bytes = None,
    bytearray_: bytearray = None,
    bool_: bool = None,
    float_: float = None,
    none_: None = None,
    class_: type = None,
    recursive: dict[str, Union[list[tuple[bytes, bool]], float]] = None,
    **kwargs,
) -> tuple[str, int, list[int], dict[str, int], tuple[int, str], set[int], frozenset[int], bytes, bytearray, bool, float, None, type, dict[str, Union[list[tuple[bytes, bool]], float]], float]:
    """A time-consuming function."""
    
    return str_, int_, list_, dict_, tuple_, set_, frozenset_, bytes_, bytearray_, bool_, float_, none_, class_, recursive, random.random()

async def _async_time_consuming_function(
    str_: str = None,
    int_: int = None,
    list_: list[int] = None,
    dict_: dict[str, int] = None,
    tuple_: tuple[int, str] = None,
    set_: set[int] = None,
    frozenset_: frozenset[int] = None,
    bytes_: bytes = None,
    bytearray_: bytearray = None,
    bool_: bool = None,
    float_: float = None,
    none_: None = None,
    class_: type = None,
    recursive: dict[str, Union[list[tuple[bytes, bool]], float]] = None,
) -> tuple[str, int, list[int], dict[str, int], tuple[int, str], set[int], frozenset[int], bytes, bytearray, bool, float, None, type, dict[str, Union[list[tuple[bytes, bool]], float]], float]:
    """A time-consuming function."""
    
    return str_, int_, list_, dict_, tuple_, set_, frozenset_, bytes_, bytearray_, bool_, float_, none_, class_, recursive, random.random()

def _time_consuming_generator_function(x: int) -> Generator[int, None, None]:
    """A time-consuming generator function."""
    
    for i in range(x):
        yield i

async def _async_time_consuming_generator_function(x: int) -> AsyncGenerator[int, None]:
    """A time-consuming generator function."""
    
    for i in range(x):
        yield i

class _TimeConsumingClass:
    def _time_consuming_function(
        self,
        *args,
        str_: str = None,
        int_: int = None,
        list_: list[int] = None,
        dict_: dict[str, int] = None,
        tuple_: tuple[int, str] = None,
        set_: set[int] = None,
        frozenset_: frozenset[int] = None,
        bytes_: bytes = None,
        bytearray_: bytearray = None,
        bool_: bool = None,
        float_: float = None,
        none_: None = None,
        class_: type = None,
        recursive: dict[str, Union[list[tuple[bytes, bool]], float]] = None,
        **kwargs,
    ) -> tuple[str, int, list[int], dict[str, int], tuple[int, str], set[int], frozenset[int], bytes, bytearray, bool, float, None, type, dict[str, Union[list[tuple[bytes, bool]], float]], float]:
        """A time-consuming function."""
        
        return str_, int_, list_, dict_, tuple_, set_, frozenset_, bytes_, bytearray_, bool_, float_, none_, class_, recursive, random.random()
    
    async def _async_time_consuming_function(
        self,
        str_: str = None,
        int_: int = None,
        list_: list[int] = None,
        dict_: dict[str, int] = None,
        tuple_: tuple[int, str] = None,
        set_: set[int] = None,
        frozenset_: frozenset[int] = None,
        bytes_: bytes = None,
        bytearray_: bytearray = None,
        bool_: bool = None,
        float_: float = None,
        none_: None = None,
        class_: type = None,
        recursive: dict[str, Union[list[tuple[bytes, bool]], float]] = None,
    ) -> tuple[str, int, list[int], dict[str, int], tuple[int, str], set[int], frozenset[int], bytes, bytearray, bool, float, None, type, dict[str, Union[list[tuple[bytes, bool]], float]], float]:
        """A time-consuming function."""
        
        return str_, int_, list_, dict_, tuple_, set_, frozenset_, bytes_, bytearray_, bool_, float_, none_, class_, recursive, random.random()

def _test_cached_function(cached_function: Callable, dir: str = None, expiry: int = None) -> None:
    """Test a cached function."""
    
    # Initialise test data.
    data = {
        'str_': 'str',
        'int_': 1,
        'list_': [1, 2, 3],
        'dict_': {'a': 1, 'b': 2, 'c': 3},
        'tuple_': (1, 'str'),
        'set_': {1, 2, 3},
        'frozenset_': frozenset({1, 2, 3}),
        'bytes_': b'bytes',
        'bytearray_': bytearray(b'bytearray'),
        'bool_': True,
        'float_': 1.0,
        'none_': None,
        'class_': type,
        'recursive': {
            'list_': [(b'bytes', True), (b'bytes', False)],
            'float_': 1.0,
        }
    }
    
    positional_data = list(data.values())
    
    # Test the caching of the time-consuming function's responses to each element of the test data.
    for field, value in data.items():
        # Test positional arguments.
        assert cached_function(value) == cached_function(value)
        
        # Test keyword arguments.
        assert cached_function(**{field: value}) == cached_function(**{field: value})
    
    # Test the caching of the time-consuming function's response to the test data as positional arguments.
    assert cached_function(*positional_data) == cached_function(*positional_data)
    
    # Test the caching of the time-consuming function's response to the test data as keyword arguments.
    assert cached_function(**data) == cached_function(**data)
    
    # Test the caching of the time-consuming function's response to the test data as a mixture of positional and keyword arguments.
    positional_data_sample = positional_data[:5]
    keyword_data_sample = {field: value for i, (field, value) in enumerate(data.items()) if i >= 5}
    assert cached_function(*positional_data_sample, **keyword_data_sample) == cached_function(*positional_data_sample, **keyword_data_sample)
    
    # Test clearing the cache.
    cached_result = cached_function(**data)
    cached_function.clear_cache()
    assert cached_function(**data) != cached_result
    
    if dir is None:
        cached_result = cached_function(**data)
        persist_cache.clear(cached_function)
        assert cached_function(**data) != cached_result

    # Test flushing the cache.
    if expiry:
        cached_result = cached_function(**data)
        time.sleep(expiry + 1)
        cached_function.flush_cache()
        assert cached_function(**data) != cached_result
        
        if dir is None:
            cached_result = cached_function(**data)
            time.sleep(expiry + 1)
            persist_cache.flush(cached_function, expiry)
            assert cached_function(**data) != cached_result

    # Test setting the time-to-live of the cache.
    cached_function.set_expiry(2)
    cached_result = cached_function(**data)
    time.sleep(3)
    assert cached_function(**data) != cached_result
    
    # Test deleting the cache if the cache's directory is known.
    if dir:
        cached_function.delete_cache()
        assert not os.path.exists(dir)

async def _async_test_cached_function(cached_function: Callable, dir: str = None, expiry: int = None) -> None:
    """Test an async cached function."""
    
    # Initialise test data.
    data = {
        'str_': 'str',
        'int_': 1,
        'list_': [1, 2, 3],
        'dict_': {'a': 1, 'b': 2, 'c': 3},
        'tuple_': (1, 'str'),
        'set_': {1, 2, 3},
        'frozenset_': frozenset({1, 2, 3}),
        'bytes_': b'bytes',
        'bytearray_': bytearray(b'bytearray'),
        'bool_': True,
        'float_': 1.0,
        'none_': None,
        'class_': type,
        'recursive': {
            'list_': [(b'bytes', True), (b'bytes', False)],
            'float_': 1.0,
        }
    }
    
    positional_data = list(data.values())
    
    # Test the caching of the time-consuming function's responses to each element of the test data.
    for field, value in data.items():
        # Test positional arguments.
        assert await cached_function(value) == await cached_function(value)
        
        # Test keyword arguments.
        assert await cached_function(**{field: value}) == await cached_function(**{field: value})
    
    # Test the caching of the time-consuming function's response to the test data as positional arguments.
    assert await cached_function(*positional_data) == await cached_function(*positional_data)
    
    # Test the caching of the time-consuming function's response to the test data as keyword arguments.
    assert await cached_function(**data) == await cached_function(**data)
    
    # Test the caching of the time-consuming function's response to the test data as a mixture of positional and keyword arguments.
    positional_data_sample = positional_data[:5]
    keyword_data_sample = {field: value for i, (field, value) in enumerate(data.items()) if i >= 5}
    assert await cached_function(*positional_data_sample, **keyword_data_sample) == await cached_function(*positional_data_sample, **keyword_data_sample)
    
    # Test clearing the cache.
    cached_result = await cached_function(**data)
    cached_function.clear_cache()
    assert await cached_function(**data) != cached_result
    
    if dir is None:
        cached_result = await cached_function(**data)
        persist_cache.clear(cached_function)
        assert await cached_function(**data) != cached_result

    # Test flushing the cache.
    if expiry:
        cached_result = await cached_function(**data)
        time.sleep(expiry + 1)
        cached_function.flush_cache()
        assert await cached_function(**data) != cached_result
        
        if dir is None:
            cached_result = await cached_function(**data)
            time.sleep(expiry + 1)
            persist_cache.flush(cached_function, expiry)
            assert await cached_function(**data) != cached_result

    # Test setting the time-to-live of the cache.
    cached_function.set_expiry(2)
    cached_result = await cached_function(**data)
    time.sleep(3)
    assert await cached_function(**data) != cached_result
    
    # Test deleting the cache if the cache's directory is known.
    if dir:
        cached_function.delete_cache()
        assert not os.path.exists(dir)

def _test_cached_generator_function(cached_generator_function: Callable, dir: str = None, expiry: int = None) -> None:
    """Test a cached generator function."""
    
    # Initialise test data.
    data = 10
    
    # Test the caching of the time-consuming generator function's responses to the test data.
    assert list(cached_generator_function(data)) == list(cached_generator_function(data))
 
async def _async_test_cached_generator_function(cached_generator_function: Callable, dir: str = None, expiry: int = None) -> None:
    """Test an async cached generator function."""
    
    # Initialise test data.
    data = 10
    
    # Test the caching of the time-consuming generator function's responses to the test data.
    y1 = []
    
    async for element in cached_generator_function(data):
        y1 += [element]
    
    y2 = []
    
    async for element in cached_generator_function(data):
        y2 += [element]
    
    assert y1 == y2

async def _test_sync_and_async_time_consuming_function(_time_consuming_function: Callable, _async_time_consuming_function: Callable) -> None:
    """Test a time-consuming function and its async equivalent."""
    
    # Cache and test the time-consuming function without arguments.
    cached_function = persist_cache.cache(_time_consuming_function)
    print('Testing the caching of the time-consuming function without arguments.')
    _test_cached_function(cached_function)

    # Cache and test the time-consuming method without arguments.
    cached_function = persist_cache.cache(_TimeConsumingClass()._time_consuming_function)
    print('Testing the caching of the time-consuming method without arguments.')
    _test_cached_function(cached_function)

    # Cache and test the async time-consuming function without arguments.
    cached_function = persist_cache.cache(_async_time_consuming_function)
    print('Testing the caching of the async time-consuming function without arguments.')
    await _async_test_cached_function(cached_function)
    
    # Cache and test the time-consuming function with arguments.
    cached_function = persist_cache.cache()(_time_consuming_function)
    print('Testing the caching of the time-consuming function with arguments.')
    _test_cached_function(cached_function)
    
    # Cache and test the async time-consuming function with arguments.
    cached_function = persist_cache.cache()(_async_time_consuming_function)
    print('Testing the caching of the async time-consuming function with arguments.')
    await _async_test_cached_function(cached_function)
    
    # Cache and test the time-consuming function with a time-to-live.
    cached_function = persist_cache.cache(expiry=1)(_time_consuming_function)
    print('Testing the caching of the time-consuming function with a time-to-live.')
    _test_cached_function(cached_function, expiry=1)
    
    # Cache and test the async time-consuming function with a time-to-live.
    cached_function = persist_cache.cache(expiry=1)(_async_time_consuming_function)
    print('Testing the caching of the async time-consuming function with a time-to-live.')
    await _async_test_cached_function(cached_function, expiry=1)
    
    # Cache and test the time-consuming function with a custom directory.
    cached_function = persist_cache.cache(dir='.custom_cache')(_time_consuming_function)
    print('Testing the caching of the time-consuming function with a custom directory.')
    _test_cached_function(cached_function, dir='.custom_cache')
    
    # Cache and test the async time-consuming function with a custom directory.
    cached_function = persist_cache.cache(dir='.custom_cache')(_async_time_consuming_function)
    print('Testing the caching of the async time-consuming function with a custom directory.')
    await _async_test_cached_function(cached_function, dir='.custom_cache')

    # Cache and test the time-consuming function with a custom name.
    cached_function = persist_cache.cache(name='.custom_function')(_time_consuming_function)
    print('Testing the caching of the time-consuming function with a custom directory.')
    _test_cached_function(cached_function, dir='.persist_cache/custom_function')
    
    # Cache and test the async time-consuming function with a custom name.
    cached_function = persist_cache.cache(name='.custom_function')(_async_time_consuming_function)
    print('Testing the caching of the async time-consuming function with a custom directory.')
    await _async_test_cached_function(cached_function, dir='.persist_cache/custom_function')
    
    # Cache and test the time-consuming generator function.
    cached_generator_function = persist_cache.cache()(_time_consuming_generator_function)
    print('Testing the caching of the time-consuming generator function.')
    _test_cached_generator_function(cached_generator_function)
    
    # Cache and test the async time-consuming generator function.
    cached_generator_function = persist_cache.cache()(_async_time_consuming_generator_function)
    print('Testing the caching of the async time-consuming generator function.')
    await _async_test_cached_generator_function(cached_generator_function)
    
    # Remove cache directories.
    for dir in {'.persist_cache', '.custom_cache'}:
        shutil.rmtree(dir, ignore_errors=True)

async def test_persist_cache() -> None:
    """Test `persist_cache.cache()`."""
    
    # Test the time-consuming function and its async equivalent.
    await _test_sync_and_async_time_consuming_function(_time_consuming_function, _async_time_consuming_function)
    
    # Test the time-consuming method and its async equivalent.
    await _test_sync_and_async_time_consuming_function(_TimeConsumingClass()._time_consuming_function, _TimeConsumingClass()._async_time_consuming_function)
import asyncio
import inspect
import os
from functools import wraps
from typing import Any, Callable
from datetime import timedelta

from . import caching
from .caching import NOT_IN_CACHE
from .helpers import inflate_arguments, signaturize


def cache(
        name: str | Callable | None = None,
        dir: str | None = None,
        expiry: int | float | timedelta | None = None,
    ) -> Callable:
    """Persistently and locally cache the returns of a function.
    
    The function to be cached must accept and return dillable objects only (with the exception of methods' `self` argument, which is always ignored). Additionally, for consistent caching across subsequent sessions, arguments and returns should also be hashable.
    
    Arguments:
        name (`str | Callable`, optional): The name of the cache (or, if `cache()` is being called as an argument-less decorator (ie, as `@cache` instead of `@cache(...)`), the function to be cached). Defaults to the hash of the qualified name of the function. If `dir` is set, this argument will be ignored.
        
        dir (`str`, optional): The directory in which the cache should be stored. Defaults to a subdirectory bearing the name of the cache in a parent folder called '.local_cache' in the current working directory.
        
        expiry (`int | float | timedelta`, optional): How long, in seconds or as a `timedelta`, function calls should persist in the cache. Defaults to `None`.
    
    Returns:
        `Callable`: If `cache()` is called with arguments, a decorator that wraps the function to be cached, otherwise, the wrapped function itself. Once wrapped, the function will have the following methods attached to it:
            - `set_expiry(value: int | float | timedelta) -> None`: Set the expiry of the cache.
            - `flush_cache() -> None`: Flush out any expired cached returns.
            - `clear_cache() -> None`: Clear out all cached returns.
            - `delete_cache() -> None`: Delete the cache."""
    
    def decorator(func: Callable) -> Callable:
        nonlocal name, dir, expiry
        
        # If the cache directory has not been set, and the name of the cache has, set it to a subdirectory by that name in a directory called '.local_cache' in the current working directory, or, if the name of the cache has not been set, set the name of that subdirectory to the hash of the qualified name of the function.
        if dir is None:
            if name is not None:
                dir = f'.local_cache/{name}'
            else:
                dir = f'.local_cache/{caching.hash(func.__qualname__)}'

        # Create the cache directory and any other necessary directories if it does not exist.
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
        
        # Flag whether the function is a method to enable the exclusion of the first argument (which will be the instance of the function's class) from being hashed to produce the cache key.
        is_method = inspect.ismethod(func)
        
        # Preserve a map of the function's arguments to their default values and the name and index of the args parameter if such a parameter exists to enable the remapping of positional arguments to their keywords, which thereby allows for the consistent caching of function calls where positional arguments are used on some occasions and keyword arguments are used on others.
        signature, args_parameter, args_i = signaturize(func)
        
        # Initialise a wrapper for synchronous functions.
        def sync_wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
            nonlocal dir, expiry, is_method
            
            # Map arguments to their keywords or the keyword of the args parameter where necessary, filtering out the first argument if the function is a method, to enable the consistent caching of function calls where positional arguments are used on some occasions and keyword arguments are used on others.
            arguments = inflate_arguments(signature, args_parameter, args_i, args[is_method:], kwargs)
            
            # Hash the arguments to produce the cache key.
            key = caching.hash(arguments)
            
            # Get the value of the key from the cache if it is not expired, otherwise, call the function and set the value of the key in the cache to the result of that call.
            if (value := caching.get(key, dir, expiry)) is NOT_IN_CACHE:
                value = func(*args, **kwargs)
                caching.set(key, value, dir)
            
            return value
        
        # Initialise a wrapper for asynchronous functions.
        async def async_wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
            nonlocal dir, expiry, is_method
            
            # Map arguments to their keywords or the keyword of the args parameter where necessary, filtering out the first argument if the function is a method, to enable the consistent caching of function calls where positional arguments are used on some occasions and keyword arguments are used on others.
            arguments = inflate_arguments(signature, args_parameter, args_i, args[is_method:], kwargs)
            
            # Hash the arguments to produce the cache key.
            key = caching.hash(arguments)
            
            # Get the value of the key from the cache if it is not expired, otherwise, call the function and set the value of the key in the cache to the result of that call.
            if (value := caching.get(key, dir, expiry)) is NOT_IN_CACHE:
                value = await func(*args, **kwargs)
                caching.set(key, value, dir)
            
            return value
        
        # Identify the appropriate wrapper for the function by checking whether it is asynchronous or not.
        wrapper = async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        
        # Attach convenience functions to the wrapper for modifying the cache.
        def delete_cache() -> None:
            """Delete the cache."""
            nonlocal dir
            
            caching.delete(dir)
        
        def clear_cache() -> None:
            """Clear the cache."""
            nonlocal dir
            
            caching.clear(dir)
        
        def flush_cache() -> None:
            """Flush expired keys from the cache."""
            nonlocal dir, expiry, is_method
            
            caching.flush(dir, expiry)
        
        def set_expiry(value: int) -> None:
            """Set the expiry of the cache."""
            nonlocal expiry
            
            expiry = value
        
        wrapper.delete_cache = delete_cache
        wrapper.clear_cache = clear_cache
        wrapper.cache_clear = wrapper.clear_cache # Add an alias for cache_clear which is used by lru_cache.
        wrapper.flush_cache = flush_cache
        wrapper.set_expiry = set_expiry
                
        # Preserve the original function.
        wrapper.__wrapped__ = func
        
        # Preserve the function's original signature.
        wrapper = wraps(func)(wrapper)
        
        return wrapper
    
    # If the first argument is a function and all of the other arguments are `None`, indicating that this decorator factory was invoked without passing any arguments, return the result of passing that function to the decorator while also emptying the first argument to avoid it being used by the decorator.
    if callable(name) and dir is expiry is None:
        func = name
        name = None
        
        return decorator(func)
    
    return decorator
# persist-cache
<a href="https://pypi.org/project/persist-cache/" alt="PyPI Version"><img src="https://img.shields.io/pypi/v/persist-cache"></a> <a href="https://github.com/umarbutler/persist-cache/actions/workflows/ci.yml" alt="Build Status"><img src="https://img.shields.io/github/actions/workflow/status/umarbutler/persist-cache/ci.yml?branch=main"></a> <a href="https://app.codecov.io/gh/umarbutler/persist-cache" alt="Code Coverage"><img src="https://img.shields.io/codecov/c/github/umarbutler/persist-cache"></a> <!-- <a href="https://pypistats.org/packages/persist-cache" alt="Downloads"><img src="https://img.shields.io/pypi/dm/persist-cache"></a> -->

`persist-cache` is an *easy-to-use* Python library for lightning-fast persistent function caching. It is capable of caching both synchronous and asynchronous functions as well as methods, and is also process-safe and thread-safe.

## Features 🎯
- **⚡ Lightning-fast**: a function call can be cached in as little as 145 microseconds and be returned back in as few as 95 microseconds.
- **💽 Persistent**: cached returns persist across sessions and are stored locally.
- **⌛ Stale-free**: cached returns may be given shelf lives, after which they will be automatically flushed out.
- **🦺 Process- and thread-safe**: interprocess file locks prevent processes and threads from writing over each other.
- **⏱️ Async-compatible**: asynchronous functions can be cached with the same decorator as synchronous ones.
- **👨‍🏫 Class-compatible**: methods can be cached with the same decorator as functions (although the `self` argument will always be ignored).

## Installation 📦
`persist-cache` may be installed with `pip`:
```bash
pip install persist-cache
```

## Usage 👩‍💻
The code snippet below demonstrates how both synchronous and asynchronous functions as well as methods can be cached with `persist-cache`:
```python
from persist_cache import cache

@cache
def my_function(): ...

@cache
async def my_function(): ...

class MyClass:
    @cache
    def my_method(self): ...
```

It is also possible to name caches and specify their shelf lives:
```python
from datetime import timedelta

@cache(name='my_shared_cache', expiry=timedelta(months=1))
def my_function(): ...

@cache(name='my_shared_cache', expiry=60 * 60 * 24 * 30)
def my_other_function(): ...
```

Once created, cached functions can be managed as follows:
```python
my_function.set_expiry(60 * 60) # Change cached returns to expire after an hour.
my_function.flush_cache() # Flush out any expired cached returns.
my_function.clear_cache() # Clear out all cached returns.
my_function.delete_cache() # Delete the cache.
```

## API 🧩
### `cache()`
```python
def cache(
    name: str | Callable | None = None,
    dir: str | None = None,
    expiry: int | float | timedelta | None = None,
) -> None
```

`cache()` persistently and locally cache the returns of a function.
    
The function to be cached must accept and return [dillable](https://dill.readthedocs.io/en/latest/) objects only (with the exception of methods' `self` argument, which is always ignored). Additionally, for consistent caching across subsequent sessions, arguments and returns should also be hashable.
    
`name` represents the name of the cache (or, if `cache()` is being called as an argument-less decorator (ie, as `@cache` instead of `@cache(...)`), the function to be cached). It defaults to the hash of the qualified name of the function. If `dir` is set, `name` will be ignored.

`dir` represents the directory in which the cache should be stored. It defaults to a subdirectory bearing the name of the cache in a parent folder called '.persist_cache' in the current working directory.
        
`expiry` represents how long, in seconds or as a `timedelta`, function calls should persist in the cache. It defaults to `None`.

If `cache()` is called with arguments, a decorator that wraps the function to be cached will be returned, otherwise, the wrapped function itself will be returned.

After being wrapped, the cached function will have the following methods attached to it:
- `set_expiry(value: int | float | timedelta) -> None`: Sets the expiry of the cache.
- `flush_cache() -> None`: Flushes out any expired cached returns.
- `clear_cache() -> None`: Clears out all cached returns.
- `delete_cache() -> None`: Deletes the cache.

## License 📜
This library is licensed under the [MIT License](https://github.com/umarbutler/persist-cache/blob/main/LICENCE).
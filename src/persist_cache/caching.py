import os
import shutil
from datetime import datetime, timedelta
from typing import Any, Union

from filelock import FileLock
from xxhash import xxh3_64_hexdigest, xxh3_128_hexdigest

from .serialization import deserialize, serialize

NOT_IN_CACHE = object()
"""A sentinel object that flags that a key is not in the cache."""

def set(key: str, value: Any, dir: str) -> None:
    """Set the given key of the provided cache to the specified value."""
    
    path = f'{dir}/{key}.msgpack'
    
    # Lock the entry before writing to it.
    with FileLock(f'{path}.lock'), \
        open(path, 'wb') as file:
            file.write(serialize(value))

def get(key: str, dir: str, expiry: Union[int, float, timedelta, None] = None) -> Any:
    """Get the value of the given key from the provided cache if it is not expired."""
    
    path = f'{dir}/{key}.msgpack'

    # If the key does not exist in the cache, return `NOT_IN_CACHE`.
    if not os.path.exists(path):
        return NOT_IN_CACHE

    # Lock the entry.
    with FileLock(f'{path}.lock'):
        # Handle expiry if necessary.
        if expiry is not None:
            # Get the time at which the key was last set.
            timestamp = os.path.getmtime(path)

            # If the entry is expired, remove it from the cache and return `NOT_IN_CACHE`.
            if isinstance(expiry, timedelta) and datetime.fromtimestamp(timestamp) + expiry < datetime.now() \
            or timestamp + expiry < datetime.now().timestamp():
                # Remove the entry.
                os.remove(path)

                return NOT_IN_CACHE
        
        # Read, deserialize and return the value.
        with open(path, 'rb') as file:
                return deserialize(file.read())

def hash(data: Any) -> str:
    """Hash the given data."""

    # Serialise the data.
    data = serialize(data)
    
    # Hash the data and affix its length, preceded by a hyphen (to reduce the likelihood of collisions).
    return f'{xxh3_128_hexdigest(data)}{len(data)}'

def shorthash(data: Any) -> str:
    """Hash the given data."""
    
    # Serialise the data.
    data = serialize(data)
    
    # Hash the data and affix its length, preceded by a hyphen (to reduce the likelihood of collisions).
    return f'{xxh3_64_hexdigest(data)}{len(data)}'

def delete(dir: str) -> None:
    """Delete the provided cache."""
    
    # Remove the cache directory and all its contents.
    shutil.rmtree(dir, ignore_errors=True)

def clear(dir: str) -> None:
    """Clear the provided cache."""
    
    # Delete the cache.
    delete(dir)
    
    # Recreate the cache directory.
    os.makedirs(dir, exist_ok=True)

def flush(dir: str, expiry: Union[int, float, timedelta, None]) -> None:
    """Flush expired keys from the provided cache."""
    
    # Iterate over keys in the cache.
    for file in os.listdir(dir):
        if not file.endswith('.msgpack'):
            continue
        
        path = f'{dir}/{file}'
        
        # Lock the entry before reading it.
        with FileLock(f'{path}.lock'):
            # Get the time at which the key was last set.
            timestamp = os.path.getmtime(path)
            
            # If the entry is expired, remove it from the cache.
            if (isinstance(expiry, timedelta) and datetime.fromtimestamp(timestamp) + expiry < datetime.now()) \
            or (timestamp + expiry < datetime.now().timestamp()):
                os.remove(path)
"""Benchmark persist-cache against other popular persistent caching libraries."""
import os
import random
import shutil
import time
from typing import Callable

import cachier
import locache
from joblib import Memory

import persist_cache


def get_size(path: str) -> int:
    """Get the size of a file or directory."""
    
    if os.path.isfile(path):
        return os.path.getsize(path)
    
    size = 0
    
    for subpath in os.listdir(path):
        subpath = os.path.join(path, subpath)
        
        if os.path.isfile(subpath):
            size += os.path.getsize(subpath)
        
        else:
            size += get_size(subpath)
    
    return size


def time_consuming_function(seed: int) -> float:
    random.seed(seed)
    return random.randint(0, 100000)

def time_function(func: Callable, iterations: int) -> float:
    """Time an instance of the time consuming function."""

    time_taken = 0
    
    for i in range(iterations):
        start = time.perf_counter()
        func(i)
        time_taken += time.perf_counter() - start
            
    return time_taken

# Initialise a `joblib.Memory` instance.
memory = Memory(".joblib", verbose=0)

# Map cachers to themselves wrapped around the time consuming function, functions to remove their caches and the names of their cache directories.
cachers = {
    'persist-cache': (
        persist_cache.cache(time_consuming_function),
        lambda cache: cache.clear_cache(),
        '.persist_cache',
    ),

    'cachier': (
        cachier.cachier(cache_dir='.cachier')(time_consuming_function),
        lambda cache: cache.clear_cache(),
        '.cachier',
    ),
    
    'joblib': (
        memory.cache(time_consuming_function),
        lambda _: memory.clear(),
        '.joblib',
    ),
    
    'locache': (
        locache.persist(time_consuming_function),
        lambda _: shutil.rmtree(locache._prepare_cache_location(time_consuming_function), ignore_errors=True) if os.path.exists(locache._prepare_cache_location(time_consuming_function)) else None,
        locache._prepare_cache_location(time_consuming_function),
    )
}

if __name__ == '__main__':
    benchmarks = []
    iterations = 10000
    
    uncached_time = time_function(time_consuming_function, iterations)/iterations
    
    for cacher, (func, emptier, dir) in cachers.items():
        print(f'=== {cacher} ===')        
        # Time how long it take to cache a function call.
        set_time = time_function(func, iterations)
        print(f'Average set time: {(set_time/iterations)-uncached_time} seconds')
        
        # Time how long it takes to retrieve a cached function call.
        get_time = time_function(func, iterations)
        print(f'Average get time: {get_time/iterations} seconds')

        # Get the size of the cache.
        print(f'Bytes used: {get_size(dir)}')
        
        print()

        # Empty the cache.
        emptier(func)
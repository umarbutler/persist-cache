## Changelog 🔄
All notable changes to `persist-cache` will be documented here. This project adheres to [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
- Stale calls are now flushed when initialising a cache.

### Changed
- Switched hashing algorithm from `XXH3` to `XXH128` and began suffixing hashes with the length of their input to significantly reduce the already very low likelihood of hash collisions.
- Pickle data is now compressed with LZ4 to speed up IO and reduce disk usage.

### Removed
- Removed unused import of `asyncio` in `persist_cache.py`.

## [0.1.1] - 2024-03-14
### Added
- Added a unit test for passing a custom name to `cache()`.
- Added unit tests for the caching of asynchronous functions and methods.
- Added unit tests for the caching of synchronous methods.

### Fixed
- Fixed `cache()`'s inability to identify certain wrapped asynchronous functions and methods as being asynchronous ([#1](https://github.com/umarbutler/persist-cache/issues/1)) ([fe7aa6c](https://github.com/umarbutler/persist-cache/commit/fe7aa6ccd2f7fbeebaa53e4c1cc0230f6ef35cb4)).
- Fixed `cache()`'s inability to cache function calls returning `bytes`, `bytearray` and `memoryview` objects ([#2](https://github.com/umarbutler/persist-cache/issues/2)) ([f763ce7](https://github.com/umarbutler/persist-cache/commit/f763ce7040c8048112dc93b59991bbcf943cc33a)).

## [0.1.0] - 2024-03-12
### Added
- Added the `cache()` decorator, which locally and persistently caches functions.

[0.1.1]: https://github.com/umarbutler/persist-cache/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/umarbutler/persist-cache/releases/tag/v0.1.0
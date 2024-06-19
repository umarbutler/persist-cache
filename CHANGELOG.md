## Changelog 🔄
All notable changes to `persist-cache` will be documented here. This project adheres to [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.3] - 2024-06-18
### Fixed
- Fixed a typo that caused the fix for [#6](https://github.com/umarbutler/persist-cache/pull/6) to not work and instead break `flush()`.

## [0.4.2] - 2024-06-18
### Fixed
- Fixed a bug wherein `flush()` would try locking lock files ([#6](https://github.com/umarbutler/persist-cache/pull/6)).
- Fixed typo in the docstring for the `test_persist_cache()` unit test in `test_persist_cache.py`.

## [0.4.1] - 2024-06-10
### Fixed
- Fixed the formatting of the docstring of `cache()` because a portion of it was being rendered by Vscode as a single line instead of a bullet point list.

## [0.4.0] - 2024-05-06
## Added
- Added support for the caching of both synchronous and asynchronous generator functions.
- Added `delete()`, `clear()` and `flush()` helper functions for deleting, clearing and flushing caches.

## [0.3.2] - 2024-03-21
### Changed
- Began hashing the names of caches with `XXH3` to ensure caches may be assigned any arbitrary name, regardless of whether it is compatible with the local file system.

## [0.3.1] - 2024-03-20
### Fixed
- Fixed a bug causing `cache()` to raise a `TypeError` when attempting to cache a function call that contains an argument that is a list containing a dictionary ([#4](https://github.com/umarbutler/persist-cache/issues/4)) ([ec07874](https://github.com/umarbutler/persist-cache/commit/ec07874)).

## [0.3.0] - 2024-03-19
### Changed
- Ceased delimiting hashes and the length of the input with hyphens as the hashes already have a fixed size so there is no possibility of collision.

## [0.2.0] - 2024-03-18
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

[0.4.3]: https://github.com/umarbutler/persist-cache/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/umarbutler/persist-cache/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/umarbutler/persist-cache/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/umarbutler/persist-cache/compare/v0.3.2...v0.4.0
[0.3.2]: https://github.com/umarbutler/persist-cache/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/umarbutler/persist-cache/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/umarbutler/persist-cache/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/umarbutler/persist-cache/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/umarbutler/persist-cache/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/umarbutler/persist-cache/releases/tag/v0.1.0
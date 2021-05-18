# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.8] - 2021-05-18

### Added

- python 3.9 support

### Changed

- removed ipython from dev dependencies
- fixed 3.6 quirks in CI
- capture decode errors too, thx @rcyrus

## [0.1.7] - 2020-12-13

### Changed

- switched to poetry for everything
- bumped mypy for py 3.9
- security fixes

## [0.1.6] - 2020-02-24

### Changed

- Expose whole jwt session cookie to starlette request.session (ie. `exp` claim is now visible).
- Adopted [Keep a Changelog](http://keepachangelog.com/) changelog format.

## [0.1.5] - 2020-02-21

### Changed

- Phased out `__version__` in module, there is no a sane way to keep it up to
- date anyway.

## [0.1.4] - 2020-02-21

### Fixed

- Python 3.6 namedtuple lack `default` parameter.

## [0.1.3] - 2020-02-21

### Added

- A changelog.
- Added linting in CI.

### Changed

- Correctly implemented ES* and RS* algorithms.

[Unreleased]: https://github.com/aogier/starlette-authlib/compare/0.1.8...HEAD
[0.1.8]: https://github.com/aogier/starlette-authlib/compare/0.1.7...0.1.8
[0.1.7]: https://github.com/aogier/starlette-authlib/compare/0.1.6...0.1.7
[0.1.6]: https://github.com/aogier/starlette-authlib/compare/0.1.5...0.1.6
[0.1.5]: https://github.com/aogier/starlette-authlib/compare/0.1.4...0.1.5
[0.1.4]: https://github.com/aogier/starlette-authlib/compare/0.1.3...0.1.4
[0.1.3]: https://github.com/aogier/starlette-authlib/releases/tag/0.1.3

[//]: # (C3-2-DKAC:GGH:Raogier/starlette-authlib:T{t})

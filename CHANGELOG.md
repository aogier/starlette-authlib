# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- drop discontinued lgtm.com service
- remove useless uvicorn dependency

## [0.1.19] - 2022-12-06

### Changed

- bump authlib requirement

## [0.1.18] - 2022-12-05

### Changed

- bump autoflake requirement
- bump starlette requirement
- introducing python 3.11

## [0.1.17] - 2022-11-20

### Changed

- bump uvicorn requirement

## [0.1.16] - 2022-11-17

### Added

- bump starlette requirement

## [0.1.15] - 2022-11-16

### Changed

- bumped dev dependencies

### Security

- bumped cryptography

## [0.1.14] - 2022-10-20

### Changed

- bumped uvicorn dependency

## [0.1.13] - 2022-09-28

### Changed

- starlette dependency bumped

## [0.1.12] - 2022-07-31

### Changed

- dev dependencies bump
- uvicorn dependency bumped to current minor

## [0.1.11] - 2022-06-13

### Changed

- dev dependencies bumps

## [0.1.10] - 2022-05-28

### Changed

- pytest version bump
- pytest-cov
- enabled codecov from the docker build
- authlib dependency bump

### Removed

- deprecated poetry-version

## [0.1.9] - 2022-05-14

### Added

- github actions workflows

### Changed

- more flexible dependencies specification for the three main libraries (authlib, uvicorn, starlette)
- dev dependencies bumps
- better project metadata in `pyproject.toml`
- minor isort reformatting

### Removed

- travis CI config

### Fixed

- type annotations for newer libraries version

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

[Unreleased]: https://github.com/aogier/starlette-authlib/compare/0.1.19...HEAD
[0.1.19]: https://github.com/aogier/starlette-authlib/compare/0.1.18...0.1.19
[0.1.18]: https://github.com/aogier/starlette-authlib/compare/0.1.17...0.1.18
[0.1.17]: https://github.com/aogier/starlette-authlib/compare/0.1.16...0.1.17
[0.1.16]: https://github.com/aogier/starlette-authlib/compare/0.1.15...0.1.16
[0.1.15]: https://github.com/aogier/starlette-authlib/compare/0.1.14...0.1.15
[0.1.14]: https://github.com/aogier/starlette-authlib/compare/0.1.13...0.1.14
[0.1.13]: https://github.com/aogier/starlette-authlib/compare/0.1.12...0.1.13
[0.1.12]: https://github.com/aogier/starlette-authlib/compare/0.1.11...0.1.12
[0.1.11]: https://github.com/aogier/starlette-authlib/compare/0.1.10...0.1.11
[0.1.10]: https://github.com/aogier/starlette-authlib/compare/0.1.9...0.1.10
[0.1.9]: https://github.com/aogier/starlette-authlib/compare/0.1.8...0.1.9
[0.1.8]: https://github.com/aogier/starlette-authlib/compare/0.1.7...0.1.8
[0.1.7]: https://github.com/aogier/starlette-authlib/compare/0.1.6...0.1.7
[0.1.6]: https://github.com/aogier/starlette-authlib/compare/0.1.5...0.1.6
[0.1.5]: https://github.com/aogier/starlette-authlib/compare/0.1.4...0.1.5
[0.1.4]: https://github.com/aogier/starlette-authlib/compare/0.1.3...0.1.4
[0.1.3]: https://github.com/aogier/starlette-authlib/releases/tag/0.1.3

[//]: # (C3-2-DKAC:GGH:Raogier/starlette-authlib:T{t})

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.10] - 2025-03-06

### Changed

- bump authlib dependency

## [0.3.9] - 2025-02-22

### Changed

- bump starlette dependency

## [0.3.8] - 2024-12-31

### Changed

- bump starlette dependency

## [0.3.7] - 2024-12-28

### Changed

- bump starlette dependency

## [0.3.6] - 2024-12-20

### Changed

- bump authlib dependency

## [0.3.5] - 2024-12-15

### Changed

- bump starlette dependency

## [0.3.4] - 2024-10-15

### Changed

- bump starlette dependency

## [0.3.3] - 2024-10-15

### Changed

- bump starlette dependency

## [0.3.2] - 2024-09-23

### Changed

- bump starlette dependency

## [0.3.1] - 2024-07-20

### Changed

- bump starlette dependency

## [0.3.0] - 2024-06-28

### Changed

- dropped python 3.7 support

## [0.2.1] - 2024-06-23

### Fixed

- missing parenthesis

## [0.2.0] - 2024-06-23

### Added

- configurable session cookie path - [#239](https://github.com/aogier/starlette-authlib/issues/239)

## [0.1.40] - 2024-04-14

### Changed

- bump starlette dependency

## [0.1.39] - 2024-03-25

### Security

- starlette bump

## [0.1.38] - 2024-02-05

### Changed

- bump starlette dependency

## [0.1.37] - 2024-01-23

### Changed

- bump starlette dependency

## [0.1.36] - 2024-01-11

### Changed

- bump starlette dependency

## [0.1.35] - 2023-12-22

### Added

- license added

## [0.1.34] - 2023-12-18

### Changed

- bump authlib dependency

## [0.1.33] - 2023-12-16

### Changed

- bump starlette dependency
- bumps dev deps

## [0.1.32] - 2023-12-01

### Changed

- bump starlette dependency

## [0.1.31] - 2023-11-05

### Changed

- bump starlette requirement

## [0.1.30] - 2023-08-26

### Fixed

- #175 honor nbf claim (lannuttia)

## [0.1.29] - 2023-07-24

### Changed

- bump starlette requirement

## [0.1.28] - 2023-07-13

### Changed

- bump starlette requirement

## [0.1.27] - 2023-07-13

### Changed

- bump starlette requirement

## [0.1.26] - 2023-07-01

### Added

- sample app enhancements

### Deprecated

- python 3.7 support will be removed on 2024-06-27

### Removed

- py3.7: no longer run checks

## [0.1.25] - 2023-06-07

### Changed

- bump starlette requirement

## [0.1.24] - 2023-05-16

### Changed

- bump starlette requirement

## [0.1.23] - 2023-03-10

### Changed

- bump starlette requirement

## [0.1.22] - 2023-02-15

### Security

- bumped starlette dependency

## [0.1.21] - 2023-02-12

### Added

- bumped starlette dependency

## [0.1.20] - 2022-12-27

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

[Unreleased]: https://github.com/aogier/starlette-authlib/compare/0.3.10...HEAD
[0.3.10]: https://github.com/aogier/starlette-authlib/compare/0.3.9...0.3.10
[0.3.9]: https://github.com/aogier/starlette-authlib/compare/0.3.8...0.3.9
[0.3.8]: https://github.com/aogier/starlette-authlib/compare/0.3.7...0.3.8
[0.3.7]: https://github.com/aogier/starlette-authlib/compare/0.3.6...0.3.7
[0.3.6]: https://github.com/aogier/starlette-authlib/compare/0.3.5...0.3.6
[0.3.5]: https://github.com/aogier/starlette-authlib/compare/0.3.4...0.3.5
[0.3.4]: https://github.com/aogier/starlette-authlib/compare/0.3.3...0.3.4
[0.3.3]: https://github.com/aogier/starlette-authlib/compare/0.3.2...0.3.3
[0.3.2]: https://github.com/aogier/starlette-authlib/compare/0.3.1...0.3.2
[0.3.1]: https://github.com/aogier/starlette-authlib/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/aogier/starlette-authlib/compare/0.2.1...0.3.0
[0.2.1]: https://github.com/aogier/starlette-authlib/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/aogier/starlette-authlib/compare/0.1.40...0.2.0
[0.1.40]: https://github.com/aogier/starlette-authlib/compare/0.1.39...0.1.40
[0.1.39]: https://github.com/aogier/starlette-authlib/compare/0.1.38...0.1.39
[0.1.38]: https://github.com/aogier/starlette-authlib/compare/0.1.37...0.1.38
[0.1.37]: https://github.com/aogier/starlette-authlib/compare/0.1.36...0.1.37
[0.1.36]: https://github.com/aogier/starlette-authlib/compare/0.1.35...0.1.36
[0.1.35]: https://github.com/aogier/starlette-authlib/compare/0.1.34...0.1.35
[0.1.34]: https://github.com/aogier/starlette-authlib/compare/0.1.33...0.1.34
[0.1.33]: https://github.com/aogier/starlette-authlib/compare/0.1.32...0.1.33
[0.1.32]: https://github.com/aogier/starlette-authlib/compare/0.1.31...0.1.32
[0.1.31]: https://github.com/aogier/starlette-authlib/compare/0.1.30...0.1.31
[0.1.30]: https://github.com/aogier/starlette-authlib/compare/0.1.29...0.1.30
[0.1.29]: https://github.com/aogier/starlette-authlib/compare/0.1.28...0.1.29
[0.1.28]: https://github.com/aogier/starlette-authlib/compare/0.1.27...0.1.28
[0.1.27]: https://github.com/aogier/starlette-authlib/compare/0.1.26...0.1.27
[0.1.26]: https://github.com/aogier/starlette-authlib/compare/0.1.25...0.1.26
[0.1.25]: https://github.com/aogier/starlette-authlib/compare/0.1.24...0.1.25
[0.1.24]: https://github.com/aogier/starlette-authlib/compare/0.1.23...0.1.24
[0.1.23]: https://github.com/aogier/starlette-authlib/compare/0.1.22...0.1.23
[0.1.22]: https://github.com/aogier/starlette-authlib/compare/0.1.21...0.1.22
[0.1.21]: https://github.com/aogier/starlette-authlib/compare/0.1.20...0.1.21
[0.1.20]: https://github.com/aogier/starlette-authlib/compare/0.1.19...0.1.20
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

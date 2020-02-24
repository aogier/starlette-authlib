# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/).


## Unreleased
---

### New

### Changes

### Fixes

### Breaks

## 0.1.6 - 2020-02-24

### Changes

* Expose whole jwt session cookie to starlette request.session (ie. `exp` claim is
  now visible).
* Adopted [Keep a Changelog](http://keepachangelog.com/) changelog format.

## 0.1.5 - 2020-02-21

### Changes

* Phased out `__version__` in module, there is no a sane way to keep it up to
  date anyway.

## 0.1.4 - 2020-02-21

### Fixes

* Python 3.6 namedtuple lack `default` parameter.

## 0.1.3 - 2020-02-21

### New

* A changelog.
* Added linting in CI.

### Changes

* Correctly implemented ES* and RS* algorithms.

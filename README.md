# Starlette Authlib Middleware

[![Build Status](https://travis-ci.org/aogier/starlette-authlib.svg?branch=master)](https://travis-ci.org/aogier/starlette-authlib)
[![codecov](https://codecov.io/gh/aogier/starlette-authlib/branch/master/graph/badge.svg)](https://codecov.io/gh/aogier/starlette-authlib)
[![Package version](https://badge.fury.io/py/starlette-authlib.svg)](https://pypi.org/project/starlette-authlib)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/aogier/starlette-authlib.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/aogier/starlette-authlib/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/aogier/starlette-authlib.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/aogier/starlette-authlib/context:python)
![PyPI - Downloads](https://img.shields.io/pypi/dm/starlette-authlib)

## Introduction

A drop-in replacement for Starlette session middleware, using [authlib's jwt](https://docs.authlib.org/en/latest/jose/jwt.html)

## Requirements

* Python 3.7+
* Starlette 0.9+

## Installation

```console
pip install starlette-authlib
```

## Usage

A complete example where we drop-in replace standard session middleware:

```python
from starlette.applications import Starlette

from starlette_authlib.middleware import AuthlibMiddleware as SessionMiddleware


app = Starlette()

app.add_middleware(SessionMiddleware, secret='secret')
```

Other things you can configure either via environment variables or `.env` file:

* `DOMAIN` - declare cookie domain. App must be under this domain. If empty,
  the cookie is restricted to the subdomain of the app (this is useful when you
  write eg. SSO portals)
* `JWT_ALG` - one of authlib JWT [supported algorithms](https://docs.authlib.org/en/latest/specs/rfc7518.html#specs-rfc7518)
* `JWT_SECRET` - jwt secret. Only useful for HS* algorithms, see the
  `sample_app` folder for middleware usage w/ crypto keys.

## Contributing

This project is absolutely open to contributions so if you have a nice idea,
create an issue to let the community discuss it.

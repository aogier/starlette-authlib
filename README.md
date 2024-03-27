# Starlette Authlib Middleware

[![codecov](https://codecov.io/gh/aogier/starlette-authlib/branch/master/graph/badge.svg)](https://codecov.io/gh/aogier/starlette-authlib)
[![Package version](https://badge.fury.io/py/starlette-authlib.svg)](https://pypi.org/project/starlette-authlib)
![PyPI - Downloads](https://img.shields.io/pypi/dm/starlette-authlib)

## Introduction

A drop-in replacement for Starlette session middleware, using [authlib's jwt](https://docs.authlib.org/en/latest/jose/jwt.html).

## Rationale

It is sometimes necessary to integrate a Starlette-based application into more
complex scenarios where other actors need to make decisions based on session
data. This middleware makes this possible by using a standard JWT token instead
of the Starlette-encrypted one, thus simplifying interaction with third-party
components.

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

app.add_middleware(SessionMiddleware, secret_key='secret')
```

Other things you can configure either via environment variables or `.env` file:

* `DOMAIN` - declare cookie domain. App must be under this domain. If empty,
  the cookie is restricted to the subdomain of the app (this is useful when you
  write eg. SSO portals)
* `JWT_ALG` - one of authlib JWT [supported algorithms](https://docs.authlib.org/en/latest/specs/rfc7518.html#specs-rfc7518)
* `JWT_SECRET` - jwt secret. Only useful for HS* algorithms, see the
  `sample_app` folder for middleware usage w/ crypto keys.

## See it in action: sample application

A sample application is included, and you can run it with either Starlette-based session middleware or this one, just by setting a variable:

```
# run with vanilla Starlette-based session middleware
VANILLA=1 uvicorn sample_app.app:app

# run with this drop-in replacement
uvicorn sample_app.app:app
```

As you can notice in code [here](sample_app/app.py), the only difference is an
import name, based on this `VANILLA` env var.

## Contributing

This project is absolutely open to contributions so if you have a nice idea,
create an issue to let the community discuss it.

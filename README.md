# Starlette Authlib Middleware

<a href="https://travis-ci.org/aogier/starlette-authlib">
    <img src="https://travis-ci.org/aogier/starlette-authlib.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/aogier/starlette-authlib">
    <img src="https://codecov.io/gh/aogier/starlette-authlib/branch/master/graph/badge.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/starlette-authlib/">
    <img src="https://badge.fury.io/py/starlette-authlib.svg" alt="Package version">
</a>

## Introduction

A drop-in replacement for Starlette session middleware, using [authlib's jwt](https://docs.authlib.org/en/latest/jose/jwt.html)

## Requirements

* Python 3.6+
* Starlette 0.9+

## Installation

```console
$ pip install starlette-authlib

...
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
* `JWT_SECRET` - jwt secret. Be aware that for non-HMAC algorithms this
  variable must point to a proper key filename

## Contributing

This project is absolutely open to contributions so if you have a nice idea,
create an issue to let the community discuss it.

# Starlette Authlib Middleware

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

## Contributing

This project is absolutely open to contributions so if you have a nice idea,
create an issue to let the community discuss it.

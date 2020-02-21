"""
Created on 20 feb 2020

@author: Alessandro Ogier <alessandro.ogier@gmail.com>

A sample demo application you can invoke with:

JWT_ALG=RS256 uvicorn sample_app.app:app

default alg is HS256

You can then check it via curl using a cookie-jar

1. "check" endpoint returns a 401

     oggei@cane ~  curl -Lv -c /tmp/cookiejar localhost:8000/
    [...]

    > GET / HTTP/1.1
    > Host: localhost:8000
    > User-Agent: curl/7.67.0
    > Accept: */*
    >
    * Mark bundle as not supporting multiuse
    < HTTP/1.1 401 Unauthorized
    < date: Fri, 21 Feb 2020 15:24:54 GMT
    < server: uvicorn
    < transfer-encoding: chunked
    <
    * Connection #0 to host localhost left intact

2. "login" endpoint correctly put you in session, and now / return http/200

     oggei@cane ~  curl -Lv -c /tmp/cookiejar localhost:8000/login
    [...]

    > GET /login HTTP/1.1
    > Host: localhost:8000
    > User-Agent: curl/7.67.0
    > Accept: */*
    >
    * Mark bundle as not supporting multiuse
    < HTTP/1.1 307 Temporary Redirect
    < date: Fri, 21 Feb 2020 15:25:44 GMT
    < server: uvicorn
    < location: http://localhost:8000/
    * Added cookie session="eyJhb[...]xHtOQ" for domain localhost, path /, expire 1583508344
    < set-cookie: session=eyJhb[...]xHtOQ; path=/; Max-Age=1209600; httponly; samesite=lax

    [...]

    > GET / HTTP/1.1
    > Host: localhost:8000
    > User-Agent: curl/7.67.0
    > Accept: */*
    > Cookie: session=eyJhb[...]xHtOQ
    >
    * Mark bundle as not supporting multiuse
    < HTTP/1.1 200 OK
    < date: Fri, 21 Feb 2020 15:25:44 GMT
    < server: uvicorn
    * Replaced cookie session="eyJhb[...]xHtOQ" for domain localhost, path /, expire 1583508344
    < set-cookie: session=eyJhb[...]xHtOQ; path=/; Max-Age=1209600; httponly; samesite=lax
    < transfer-encoding: chunked
    <
    * Connection #0 to host localhost left intact

"""

import os
from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import Secret
from starlette.responses import Response, RedirectResponse
from starlette.routing import Route

from starlette_authlib.middleware import AuthlibMiddleware, SecretKey


config = Config(".env")  # pylint: disable=invalid-name
KEYS_DIR = os.path.join(os.path.dirname(__file__), "keys")

# Override this via command line env vars eg.
# JWT_ALG=RS256 uvicorn sample_app.app:app
JWT_ALG = config("JWT_ALG", cast=str, default="HS256")


async def check(request):
    """
    Check if we are in session.
    """
    if not request.session.get("user"):
        return Response(status_code=401)

    return Response()


async def login(request):
    """
    A login endpoint that creates a session.
    """
    request.session.update(
        {"iss": "myself", "user": "username",}
    )
    return RedirectResponse(url=request.url_for("check"))


routes = [  # pylint: disable=invalid-name
    Route("/", endpoint=check, name="check"),
    Route("/login", endpoint=login),
]


app = Starlette(debug=True, routes=routes)  # pylint: disable=invalid-name

if JWT_ALG.startswith("HS"):
    secret_key = config(  # pylint: disable=invalid-name
        "JWT_SECRET", cast=Secret, default="secret"
    )
else:

    if JWT_ALG.startswith("RS"):

        private_key = open(  # pylint: disable=invalid-name
            os.path.join(KEYS_DIR, "rsa.key")
        ).read()

        public_key = open(  # pylint: disable=invalid-name
            os.path.join(KEYS_DIR, "rsa.pub")
        ).read()

    elif JWT_ALG.startswith("ES"):

        private_key = open(  # pylint: disable=invalid-name
            os.path.join(KEYS_DIR, "ec.key")
        ).read()

        public_key = open(  # pylint: disable=invalid-name
            os.path.join(KEYS_DIR, "ec.pub")
        ).read()

    ## WIP: can't find a proper way to generate them

    #     elif JWT_ALG.startswith("PS"):
    #
    #         private_key = open(  # pylint: disable=invalid-name
    #             os.path.join(KEYS_DIR, "ps.key")
    #         ).read()
    #
    #         public_key = open(  # pylint: disable=invalid-name
    #             os.path.join(KEYS_DIR, "ps.pub")
    #         ).read()

    secret_key = SecretKey(  # pylint: disable=invalid-name
        Secret(private_key), Secret(public_key)
    )

app.add_middleware(AuthlibMiddleware, secret_key=secret_key)

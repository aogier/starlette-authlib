"""
Created on 20 feb 2020

@author: Alessandro Ogier <alessandro.ogier@gmail.com>
"""

import os

from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import Secret
from starlette.responses import Response, RedirectResponse
from starlette.routing import Route

from starlette_authlib.middleware import AuthlibMiddleware

config = Config(".env")


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
    request.session.update({
        "iss": "myself",
        "user": "username",
    })
    return RedirectResponse(url=request.url_for("check"))

routes = [  # pylint: disable=invalid-name
    Route("/", endpoint=check, name="check"),
    Route("/login", endpoint=login),
]


app = Starlette(debug=True, routes=routes)  # pylint: disable=invalid-name

if config("JWT_ALG", cast=str).startswith("HS"):
    secret_key = config(  # pylint: disable=invalid-name
        "JWT_SECRET", cast=Secret)
else:
    secret_key = Secret(  # pylint: disable=invalid-name
        open(config("JWT_SECRET", cast=str)).read())

app.add_middleware(AuthlibMiddleware, secret_key=secret_key)

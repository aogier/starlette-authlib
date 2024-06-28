"""
Created on 20 feb 2020

@author: Alessandro Ogier <alessandro.ogier@gmail.com>
"""

from __future__ import annotations

import time
import typing
from collections import namedtuple

from authlib.jose import jwt
from authlib.jose.errors import (
    BadSignatureError,
    DecodeError,
    ExpiredTokenError,
    InvalidTokenError,
)
from starlette.config import Config
from starlette.datastructures import MutableHeaders, Secret
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Message, Receive, Scope, Send

config = Config(".env")

SecretKey = namedtuple("SecretKey", ("encode", "decode"))


class AuthlibMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        secret_key: typing.Union[str, Secret, SecretKey],
        session_cookie: str = "session",
        max_age: int | None = 14 * 24 * 60 * 60,  # 14 days, in seconds
        path: str = "/",
        same_site: str = "lax",
        https_only: bool = False,
        domain: typing.Optional[str] = config("DOMAIN", cast=str, default=None),
        jwt_alg: str = config("JWT_ALG", cast=str, default="HS256"),
    ) -> None:
        self.app = app

        self.jwt_header = {"alg": jwt_alg}
        if not isinstance(secret_key, SecretKey):
            self.jwt_secret = SecretKey(Secret(str(secret_key)), None)
        else:
            self.jwt_secret = secret_key

        # check crypto setup so we bail out if needed
        _jwt = jwt.encode(self.jwt_header, {"1": 2}, str(self.jwt_secret.encode))
        assert {"1": 2} == jwt.decode(
            _jwt,
            str(
                self.jwt_secret.decode
                if self.jwt_secret.decode
                else self.jwt_secret.encode
            ),
        ), "wrong crypto setup"

        self.session_cookie = session_cookie
        self.max_age = max_age
        self.path = path
        self.security_flags = "httponly; samesite=" + same_site
        if https_only:  # Secure flag can be used with HTTPS only
            self.security_flags += "; secure"
        if domain is not None:
            self.security_flags += f"; domain={domain}"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)
        initial_session_was_empty = True

        if self.session_cookie in connection.cookies:
            data = connection.cookies[self.session_cookie].encode("utf-8")
            try:
                jwt_payload = jwt.decode(
                    data,
                    str(
                        self.jwt_secret.decode
                        if self.jwt_secret.decode
                        else self.jwt_secret.encode
                    ),
                )
                jwt_payload.validate_exp(time.time(), 0)
                jwt_payload.validate_nbf(time.time(), 0)
                scope["session"] = jwt_payload
                initial_session_was_empty = False
            except (
                BadSignatureError,
                ExpiredTokenError,
                DecodeError,
                InvalidTokenError,
            ):
                scope["session"] = {}
        else:
            scope["session"] = {}

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                if scope["session"]:
                    if "exp" not in scope["session"]:
                        scope["session"]["exp"] = int(time.time()) + (
                            self.max_age if self.max_age else 0
                        )
                    data = jwt.encode(
                        self.jwt_header, scope["session"], str(self.jwt_secret.encode)
                    )

                    headers = MutableHeaders(scope=message)
                    header_value = "{session_cookie}={data}; path={path}; {max_age}{security_flags}".format(  # noqa E501
                        session_cookie=self.session_cookie,
                        data=data.decode("utf-8"),
                        path=self.path,
                        max_age=f"Max-Age={self.max_age}; " if self.max_age else "",
                        security_flags=self.security_flags,
                    )
                    headers.append("Set-Cookie", header_value)
                elif not initial_session_was_empty:
                    # The session has been cleared.
                    headers = MutableHeaders(scope=message)
                    header_value = "{session_cookie}=null; path={path}; {expires}{security_flags}".format(  # noqa E501
                        session_cookie=self.session_cookie,
                        path=self.path,
                        expires="expires=Thu, 01 Jan 1970 00:00:00 GMT; ",
                        security_flags=self.security_flags,
                    )
                    headers.append("Set-Cookie", header_value)
            await send(message)

        await self.app(scope, receive, send_wrapper)

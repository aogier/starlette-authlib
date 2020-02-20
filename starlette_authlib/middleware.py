"""
Created on 20 feb 2020

@author: Alessandro Ogier <alessandro.ogier@gmail.com>
"""
from starlette.config import Config
from starlette.datastructures import MutableHeaders, Secret
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Message, Receive, Scope, Send
import time
import typing

from authlib.jose import jwt
from authlib.jose.errors import BadSignatureError, ExpiredTokenError


config = Config(".env")


class AuthlibMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        secret_key: typing.Union[str, Secret],
        session_cookie: str = "session",
        max_age: int = 14 * 24 * 60 * 60,  # 14 days, in seconds
        same_site: str = "lax",
        https_only: bool = False,
        domain: str = config("DOMAIN", cast=str, default=None),
    ) -> None:
        self.app = app
        self.jwt_header = {"alg": config("JWT_ALG", cast=str, default="HS256")}
        self.jwt_secret = secret_key
        self.domain = domain
        self.session_cookie = session_cookie
        self.max_age = max_age
        self.security_flags = "httponly; samesite=" + same_site
        if https_only:  # Secure flag can be used with HTTPS only
            self.security_flags += "; secure"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)
        initial_session_was_empty = True

        if self.session_cookie in connection.cookies:
            data = connection.cookies[self.session_cookie].encode("utf-8")
            try:
                jwt_payload = jwt.decode(data, str(self.jwt_secret))
                jwt_payload.validate_exp(time.time(), 0)
                scope["session"] = jwt_payload["sdata"]
                initial_session_was_empty = False
            except (BadSignatureError, ExpiredTokenError):
                scope["session"] = {}
        else:
            scope["session"] = {}

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                if scope["session"]:
                    session_data = {
                        "exp": int(time.time()) + self.max_age,
                        "sdata": scope["session"],
                    }
                    data = jwt.encode(
                        self.jwt_header, session_data, str(self.jwt_secret)
                    )

                    headers = MutableHeaders(scope=message)
                    header_value = "%s=%s; path=/; Max-Age=%d; %s" % (
                        self.session_cookie,
                        data.decode("utf-8"),
                        self.max_age,
                        self.security_flags,
                    )
                    if self.domain:  # pragma: no cover
                        header_value += f"; domain={self.domain}"
                    headers.append("Set-Cookie", header_value)
                elif not initial_session_was_empty:
                    # The session has been cleared.
                    headers = MutableHeaders(scope=message)
                    header_value = "%s=%s; %s" % (
                        self.session_cookie,
                        "null; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT;",
                        self.security_flags,
                    )
                    if self.domain:  # pragma: no cover
                        header_value += f"; domain={self.domain}"
                    headers.append("Set-Cookie", header_value)
            await send(message)

        await self.app(scope, receive, send_wrapper)

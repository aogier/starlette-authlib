import os
import re
from datetime import datetime, timedelta

import pytest
from starlette.applications import Starlette
from starlette.datastructures import Secret
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route
from starlette.testclient import TestClient

from starlette_authlib.middleware import (
    AuthlibMiddleware as SessionMiddleware,
    SecretKey,
)

KEYS_DIR = os.path.join(os.path.dirname(__file__), "..", "sample_app", "keys")


def view_session(request):
    return JSONResponse({"session": request.session})


async def update_session(request):
    data = await request.json()
    request.session.update(data)
    return JSONResponse({"session": request.session})


async def clear_session(request):
    request.session.clear()
    return JSONResponse({"session": request.session})


def create_app():
    app = Starlette()
    app.add_route("/view_session", view_session)
    app.add_route("/update_session", update_session, methods=["POST"])
    app.add_route("/clear_session", clear_session, methods=["POST"])
    return app


def test_failing_session_setup():
    jwt_alg = "ES256"
    secret_key = SecretKey(
        Secret(open(os.path.join(KEYS_DIR, "ec.key")).read()),
        Secret(open(os.path.join(KEYS_DIR, "rsa.pub")).read()),
    )

    app = create_app()
    with pytest.raises(Exception):
        app.add_middleware(SessionMiddleware, jwt_alg=jwt_alg, secret_key=secret_key)
        app.build_middleware_stack()


def test_session():
    for jwt_alg, secret_key in (
        ("HS256", "example"),
        (
            "RS256",
            SecretKey(
                Secret(open(os.path.join(KEYS_DIR, "rsa.key")).read()),
                Secret(open(os.path.join(KEYS_DIR, "rsa.pub")).read()),
            ),
        ),
    ):
        app = create_app()
        app.add_middleware(SessionMiddleware, jwt_alg=jwt_alg, secret_key=secret_key)
        client = TestClient(app)

        response = client.get("/view_session")
        assert response.json() == {"session": {}}

        response = client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        # check cookie max-age
        set_cookie = response.headers["set-cookie"]
        max_age_matches = re.search(r"; Max-Age=([0-9]+);", set_cookie)
        assert max_age_matches is not None
        assert int(max_age_matches[1]) == 14 * 24 * 3600

        response = client.get("/view_session").json()
        assert "exp" in response["session"]
        del response["session"]["exp"]
        assert response == {"session": {"some": "data"}}

        response = client.post("/clear_session")
        assert response.json() == {"session": {}}

        response = client.get("/view_session")
        assert response.json() == {"session": {}}


def test_session_expires():
    for jwt_alg, secret_key in (
        ("HS256", "example"),
        (
            "RS256",
            SecretKey(
                Secret(open(os.path.join(KEYS_DIR, "rsa.key")).read()),
                Secret(open(os.path.join(KEYS_DIR, "rsa.pub")).read()),
            ),
        ),
    ):
        app = create_app()
        app.add_middleware(
            SessionMiddleware, jwt_alg=jwt_alg, secret_key=secret_key, max_age=-1
        )
        client = TestClient(app)

        response = client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        # requests removes expired cookies from response.cookies, we need to
        # fetch session id from the headers and pass it explicitly
        expired_cookie_header = response.headers["set-cookie"]
        expired_session_value = re.search(r"session=([^;]*);", expired_cookie_header)[1]

        response = client.get(
            "/view_session", cookies={"session": expired_session_value}
        )
        assert response.json() == {"session": {}}


def test_session_futue_nbf():
    now = datetime.now()
    nbf = datetime.timestamp(now + timedelta(days=1))
    claims = {"nbf": nbf, "some": "data"}
    for jwt_alg, secret_key in (
        ("HS256", "example"),
        (
            "RS256",
            SecretKey(
                Secret(open(os.path.join(KEYS_DIR, "rsa.key")).read()),
                Secret(open(os.path.join(KEYS_DIR, "rsa.pub")).read()),
            ),
        ),
    ):
        app = create_app()
        app.add_middleware(
            SessionMiddleware, jwt_alg=jwt_alg, secret_key=secret_key, https_only=True
        )
        secure_client = TestClient(app, base_url="https://testserver")

        response = secure_client.get("/view_session")
        assert response.json() == {"session": {}}

        response = secure_client.post("/update_session", json=claims.copy())
        assert response.json() == {"session": claims.copy()}

        response = secure_client.get("/view_session").json()
        assert response == {"session": {}}

        response = secure_client.post("/clear_session")
        assert response.json() == {"session": {}}

        response = secure_client.get("/view_session")
        assert response.json() == {"session": {}}


def test_session_past_nbf():
    now = datetime.now()
    nbf = datetime.timestamp(now - timedelta(seconds=1))
    claims = {"nbf": nbf, "some": "data"}
    for jwt_alg, secret_key in (
        ("HS256", "example"),
        (
            "RS256",
            SecretKey(
                Secret(open(os.path.join(KEYS_DIR, "rsa.key")).read()),
                Secret(open(os.path.join(KEYS_DIR, "rsa.pub")).read()),
            ),
        ),
    ):
        app = create_app()
        app.add_middleware(
            SessionMiddleware, jwt_alg=jwt_alg, secret_key=secret_key, https_only=True
        )
        secure_client = TestClient(app, base_url="https://testserver")

        response = secure_client.get("/view_session")
        assert response.json() == {"session": {}}

        response = secure_client.post("/update_session", json=claims.copy())
        assert response.json() == {"session": claims.copy()}

        response = secure_client.get("/view_session").json()
        assert "exp" in response["session"]
        del response["session"]["exp"]
        assert response == {"session": claims.copy()}

        response = secure_client.post("/clear_session")
        assert response.json() == {"session": {}}

        response = secure_client.get("/view_session")
        assert response.json() == {"session": {}}


def test_secure_session():
    for jwt_alg, secret_key in (
        ("HS256", "example"),
        (
            "RS256",
            SecretKey(
                Secret(open(os.path.join(KEYS_DIR, "rsa.key")).read()),
                Secret(open(os.path.join(KEYS_DIR, "rsa.pub")).read()),
            ),
        ),
    ):
        app = create_app()
        app.add_middleware(
            SessionMiddleware, jwt_alg=jwt_alg, secret_key=secret_key, https_only=True
        )
        secure_client = TestClient(app, base_url="https://testserver")
        unsecure_client = TestClient(app, base_url="http://testserver")

        response = unsecure_client.get("/view_session")
        assert response.json() == {"session": {}}

        response = unsecure_client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        response = unsecure_client.get("/view_session")
        assert response.json() == {"session": {}}

        response = secure_client.get("/view_session")
        assert response.json() == {"session": {}}

        response = secure_client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        response = secure_client.get("/view_session").json()
        assert "exp" in response["session"]
        del response["session"]["exp"]
        assert response == {"session": {"some": "data"}}

        response = secure_client.post("/clear_session")
        assert response.json() == {"session": {}}

        response = secure_client.get("/view_session")
        assert response.json() == {"session": {}}


def test_session_cookie_subpath():
    for jwt_alg, secret_key in (
        ("HS256", "example"),
        (
            "RS256",
            SecretKey(
                Secret(open(os.path.join(KEYS_DIR, "rsa.key")).read()),
                Secret(open(os.path.join(KEYS_DIR, "rsa.pub")).read()),
            ),
        ),
    ):
        second_app = Starlette(
            routes=[
                Route(
                    "/update_session",
                    endpoint=update_session,
                    methods=["POST"],
                ),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    jwt_alg=jwt_alg,
                    secret_key=secret_key,
                    path="/second_app",
                )
            ],
        )

        app = Starlette(routes=[Mount("/second_app", app=second_app)])
        client = TestClient(app, base_url="https://testserver")
        response = client.post("/second_app/update_session", json={"some": "data"})
        assert response.status_code == 200
        cookie = response.headers["set-cookie"]
        cookie_path_match = re.search(r"; path=(\S+);", cookie)
        assert cookie_path_match is not None
        cookie_path = cookie_path_match.groups()[0]
        assert cookie_path == "/second_app"


def test_domain_cookie() -> None:
    for jwt_alg, secret_key in (
        ("HS256", "example"),
        (
            "RS256",
            SecretKey(
                Secret(open(os.path.join(KEYS_DIR, "rsa.key")).read()),
                Secret(open(os.path.join(KEYS_DIR, "rsa.pub")).read()),
            ),
        ),
    ):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    jwt_alg=jwt_alg,
                    secret_key=secret_key,
                    domain=".example.com",
                )
            ],
        )
        client = TestClient(app, base_url="https://testserver")

        response = client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        # check cookie max-age
        set_cookie = response.headers["set-cookie"]
        assert "domain=.example.com" in set_cookie

        client.cookies.delete("session")
        response = client.get("/view_session")
        assert response.json() == {"session": {}}


def _forge_hs256(payload, secret):
    """Mint an HS256 JWT by hand, signing with ``secret`` as the HMAC key.

    This bypasses authlib's encoder (which refuses PEM material as an HMAC
    secret) so we can reproduce the algorithm-confusion attack against an
    asymmetric setup: an attacker signs with the public key, which is not a
    secret.
    """
    import base64
    import hashlib
    import hmac
    import json

    def b64(raw):
        return base64.urlsafe_b64encode(raw).rstrip(b"=")

    header = b64(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    body = b64(json.dumps(payload).encode())
    signing_input = header + b"." + body
    sig = b64(hmac.new(secret.encode(), signing_input, hashlib.sha256).digest())
    return (signing_input + b"." + sig).decode()


def test_rejects_algorithm_confusion():
    """An HS256 token signed with the RS256 public key must be rejected.

    Without pinning the verification algorithm, authlib would honour the
    token's own ``alg`` header and verify the HMAC against the public key,
    forging an authenticated session (CWE-347).
    """
    public_key = open(os.path.join(KEYS_DIR, "rsa.pub")).read()
    secret_key = SecretKey(
        Secret(open(os.path.join(KEYS_DIR, "rsa.key")).read()),
        Secret(public_key),
    )

    app = create_app()
    app.add_middleware(SessionMiddleware, jwt_alg="RS256", secret_key=secret_key)
    client = TestClient(app)

    forged = _forge_hs256(
        {"user": "admin", "exp": int(datetime.timestamp(datetime.now())) + 3600},
        public_key,
    )
    response = client.get("/view_session", cookies={"session": forged})

    # forgery is dropped, not honoured, and not a 500
    assert response.status_code == 200
    assert response.json() == {"session": {}}


def test_genuine_rs256_still_accepted():
    """A legitimately signed RS256 token is still verified and accepted."""
    secret_key = SecretKey(
        Secret(open(os.path.join(KEYS_DIR, "rsa.key")).read()),
        Secret(open(os.path.join(KEYS_DIR, "rsa.pub")).read()),
    )

    app = create_app()
    app.add_middleware(SessionMiddleware, jwt_alg="RS256", secret_key=secret_key)
    client = TestClient(app)

    response = client.post("/update_session", json={"some": "data"})
    assert response.json() == {"session": {"some": "data"}}
    response = client.get("/view_session").json()
    assert response["session"]["some"] == "data"

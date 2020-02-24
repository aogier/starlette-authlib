import os
import re

import pytest
from starlette.applications import Starlette
from starlette.datastructures import Secret
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from starlette_authlib.middleware import AuthlibMiddleware as SessionMiddleware
from starlette_authlib.middleware import SecretKey

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


def test_session():

    for jwt_alg, secret_key in (
        ("HS256", "example"),
        (
            "ES256",
            SecretKey(
                Secret(open(os.path.join(KEYS_DIR, "ec.key")).read()),
                Secret(open(os.path.join(KEYS_DIR, "ec.pub")).read()),
            ),
        ),
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
            "ES256",
            SecretKey(
                Secret(open(os.path.join(KEYS_DIR, "ec.key")).read()),
                Secret(open(os.path.join(KEYS_DIR, "ec.pub")).read()),
            ),
        ),
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


def test_secure_session():
    for jwt_alg, secret_key in (
        ("HS256", "example"),
        (
            "ES256",
            SecretKey(
                Secret(open(os.path.join(KEYS_DIR, "ec.key")).read()),
                Secret(open(os.path.join(KEYS_DIR, "ec.pub")).read()),
            ),
        ),
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

from src.masonite.controllers import Controller
from src.masonite.views import View
from src.masonite.response.response import Response
from src.masonite.request.request import Request


class WelcomeController(Controller):
    def show(self):
        return "welcome"

    def test(self):
        return 2 / 0

    def view(self, view: View):
        return view.render("welcome")

    def create(self):
        return "user created", 201

    def not_found(self):
        return "not found", 404

    def unauthorized(self):
        return "unauthorized", 401

    def forbidden(self):
        return "forbidden", 403

    def empty(self):
        return "", 204

    def redirect_url(self, response: Response):
        return response.redirect("/")

    def redirect_route(self, response: Response):
        return response.redirect(name="test")

    def redirect_route_params(self, response: Response):
        return response.redirect(name="test_params", params={"id": 1})

    def response_with_headers(self, response: Response):
        response.header("TEST", "value")
        response.header("TEST2", "value2")
        return ""

    def view_with_context(self, view: View):
        return view.render("welcome", {"count": 1, "users": ["John", "Joe"]})

    def json(self, response: Response):
        return response.json(
            {
                "key": "value",
                "key2": [1,2],
                "other_key": {
                    "nested": 1,
                    "nested_again": {"a": 1, "b": 2},
                },
            }
        )

    def session(self, request: Request):
        # request.session.flash("key", "value")
        request.app.make("session").driver("cookie").flash("key", "value")
        return "session"

    def session_with_errors(self, request: Request):
        request.app.make("session").driver("cookie").flash("key", "value")
        request.app.make("session").driver("cookie").flash("errors", {
            "email": "Email required",
            "password": "Password too short",
            "name": ""
        })
        return "session"

    def session2(self, request: Request):
        request.app.make("session").driver("cookie").flash("key", {
            "nested": 1,
            "nested_again": {
                "key2": "value2"
            }
        })
        return "session2"

    def with_params(self):
        return ""

    def auth(self, request: Request):
        request.app.make("auth").guard("web").attempt(

            "idmann509@gmail.com", "secret"
        )
        return "logged in"

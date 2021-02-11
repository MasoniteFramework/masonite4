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

    def create(self, view: View):
        return view.render("welcome"), 201

    def not_found(self):
        return "not found", 404

    def unauthorized(self, view: View):
        return view.render("unauthorized"), 403

    def forbidden(self, view: View):
        return view.render("forbidden"), 403

    def empty(self, view: View):
        return view.render(""), 204

    def redirect_url(self, response: Response):
        return response.redirect("/")

    def redirect_route(self, response: Response):
        return response.redirect(name="test")

    def redirect_route_params(self, response: Response):
        return response.redirect(name="test_params", params={"id": 1})

    def response_with_headers(self, response: Response):
        response.header('TEST', "value")
        response.header('TEST2', "value2")
        return

    def view_with_context(self, view: View):
        return view.render("welcome", {"count": 1, "users": ["John", "Joe"]})

    def json(self, response: Response):
        return response.json({
            "key": "value",
            "key2": "value2",
            "other_key": {
                "nested": 1,
                "other": 2,
                "nested_again": {
                    "a": 1,
                    "b": 2
                }
            }
        })

    def session(self, request: Request):
        request.session.flash("key", "value")
        return "session"

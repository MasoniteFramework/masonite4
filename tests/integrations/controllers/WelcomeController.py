from src.masonite.controllers import Controller
from src.masonite.views import View
from src.masonite.response.response import Response


class WelcomeController(Controller):
    def show(self):
        return "welcome"

    def test(self):
        return 2 / 0

    def view(self, view: View):
        return view.render("welcome")

    def create(self, view: View):
        return view("welcome", status=201)

    def not_found(self):
        return "not found", 404

    def unauthorized(self, view: View):
        return view("unauthorized", status=401)

    def forbidden(self, view: View):
        return view("forbidden", status=403)

    def empty(self, view: View):
        return view("", status=204)

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
            "other_key": {
                "nested": 1
            }
        })
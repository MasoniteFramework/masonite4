from src.masonite.controllers import Controller
from src.masonite.views import View


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

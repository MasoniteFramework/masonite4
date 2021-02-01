from src.masonite.controllers import Controller
from src.masonite.views import View


class WelcomeController(Controller):
    def show(self):
        return "welcome"

    def test(self):
        return "test"

    def view(self, view: View):
        return view.render("welcome")

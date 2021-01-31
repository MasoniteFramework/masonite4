from src.masonite.controllers import Controller


class WelcomeController(Controller):
    def show(self):
        return "welcome"

    def test(self):
        return "test"

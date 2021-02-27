from src.masonite.controllers import Controller
from src.masonite.views import View
from tests.integrations.app.User import User
from src.masonite.request import Request


class LoginController:
    def show(self, view: View):  # Show login page
        return view.render("auth.login")

    def store(self, view: View, request: Request):  # Show login page
        return User.attempt(
            request.input(request.input("username")), request.input("password")
        )

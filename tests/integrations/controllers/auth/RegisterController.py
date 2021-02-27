from src.masonite.controllers import Controller
from src.masonite.views import View
from tests.integrations.app.User import User
from src.masonite.request import Request

# from src.masonite.auth import Auth


class RegisterController:
    def show(self, view: View):  # Show login page
        return view.render("auth.register")

    def store(self):  # Show login page
        dd(auth)
        return User.attempt(
            request.input(request.input("username")), request.input("password")
        )

from src.masonite.controllers import Controller
from src.masonite.views import View
from tests.integrations.app.User import User
from src.masonite.request import Request
from src.masonite.response import Response
from src.masonite.authentication import Auth


class LoginController:
    def show(self, view: View):  # Show login page
        return view.render("auth.login")

    def store(self, view: View, request: Request, auth: Auth):  # Show login page
        login = auth.attempt(
            request.input("username"), request.input("password")
        )

        if login:
            dd(login)

        # Go back to login page
        return "logged in"

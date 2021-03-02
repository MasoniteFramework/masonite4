from src.masonite.controllers import Controller
from src.masonite.views import View
from tests.integrations.app.User import User
from src.masonite.request import Request
from src.masonite.response import Response
from src.masonite.authentication import Auth


class LoginController:
    def show(self, view: View):
        return view.render("auth.login")

    def store(self, view: View, request: Request, auth: Auth, response: Response):
        login = auth.attempt(request.input("username"), request.input("password"))

        if login:
            return response.redirect(name="auth.home")

        # Go back to login page
        return response.redirect(name="login")

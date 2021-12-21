from masonite.controllers import Controller
from masonite.request import Request
from masonite.response import Response
from masonite.authentication import Auth


class AuthenticationController(Controller):
    def auth(self, auth: Auth, request: Request, response: Response):
        user = auth.attempt(request.input("username"), request.input("password"))

        if user:
            return {"data": user.generate_jwt()}

        return response.json(
            {"message": "Could not find username or password"}, status="403"
        )

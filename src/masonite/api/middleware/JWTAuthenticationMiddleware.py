from masonite.middleware import Middleware
from masonite.facades import Auth

class JWTAuthenticationMiddleware(Middleware):

    def before(self, request, response):
        token = request.input('token')
        if not token:
            return response.view({"message": "Authentication token missing"}, status="401")

        if not Auth.guard('jwt').attempt_by_token(token):
            return response.view({"message": "Token invalid"}, status="401")

        return request
            

    def after(self, request, response):
        pass


from ..middleware import Middleware


class APIAuthenticationMiddleware(Middleware):
    def before(self, request, response):
        user = (
            request.app.make("auth")
            .guard("api")
            .attempt(request.input("api_token"), None)
        )
        if not user:
            return response.view("not authorized", 401)

        return request

    def after(self, request, response):
        return request

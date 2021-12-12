from masonite.middleware import Middleware


class CorsMiddleware(Middleware):

    headers = {}

    def before(self, request, response):
        if request.get_request_method() == "OPTIONS":
            return response.view("preflight")
        return request

    def after(self, request, response):
        response.header(self.headers)
        return request

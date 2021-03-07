from ..middleware import Middleware


class ResponseMiddleware(Middleware):
    def before(self, request, response):
        return request

    def after(self, request, response):
        if request.header("content-type") == "application/json":
            response.header("content-type", "application/json; charset=utf-8")
        return request

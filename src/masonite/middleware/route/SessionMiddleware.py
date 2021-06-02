from .. import Middleware


class SessionMiddleware(Middleware):
    def before(self, request, response):
        if not request.cookie("SESSID"):
            request.cookie("SESSID", "cookie")

        return request

    def after(self, request, response):

        return request

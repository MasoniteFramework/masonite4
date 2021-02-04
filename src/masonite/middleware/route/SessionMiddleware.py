from .. import Middleware


class SessionMiddleware(Middleware):
    def before(self, request, response):
        if not request.cookie("SESSID"):
            request.cookie("SESSID", request.app.make("sign").sign("cookie"))

        return request

    def after(self, request, response):

        return request

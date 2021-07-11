from .. import Middleware
from ...utils.helpers import random_string


class SessionMiddleware(Middleware):
    def before(self, request, response):
        if not request.cookie("SESSID"):
            session_code = random_string(10)
            response.cookie("SESSID", session_code)
            request.cookie("SESSID", session_code)
        # load session from request cookies
        request.app.make("session").start()
        return request

    def after(self, request, response):
        request.app.make("session").save()
        return request

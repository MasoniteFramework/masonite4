from .. import Middleware
from ...utils.helpers import random_string
from ...facades import Request, Session, Response


class SessionMiddleware(Middleware):
    def before(self, request, response):
        if not request.cookie("SESSID"):
            session_code = random_string(10)
            response.cookie("SESSID", session_code)
            request.cookie("SESSID", session_code)
        Session.start()
        request.app.make("response").with_input = self.with_input
        request.app.make("request").session = Session
        return request

    def after(self, request, _):
        Session.save()
        return request

    def with_input(self):
        for key, value in Request.all().items():
            Session.flash(key, value)

        return Response

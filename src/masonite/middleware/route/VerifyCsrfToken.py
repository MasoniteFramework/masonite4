from .. import Middleware


class VerifyCsrfToken(Middleware):
    def before(self, request, response):

        return request

    def after(self, request, response):

        return request

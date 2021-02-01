from .. import Middleware


class VerifyCsrfToken(Middleware):
    def before(self, request, response):
        # print(request.cookie_jar.get("csrf_token"))

        # if request.get_path() == "/":
        #     return response.redirect("/test")

        return request

    def after(self, request, response):

        return request

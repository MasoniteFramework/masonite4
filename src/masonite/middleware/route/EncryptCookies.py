from ...exceptions import InvalidToken


class EncryptCookies:
    def before(self, request, response):
        for _, cookie in request.cookie_jar.all().items():
            cookie.value = request.app.make("sign").unsign(cookie.value)

        return request

    def after(self, request, response):
        for _, cookie in response.cookie_jar.all().items():
            cookie.value = request.app.make("sign").sign(cookie.value)

        return request

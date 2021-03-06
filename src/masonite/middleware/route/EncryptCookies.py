class EncryptCookies:
    def before(self, request, response):
        for key, cookie in request.cookie_jar.all().items():
            cookie.value = request.app.make("sign").unsign(cookie.value)

    def after(self, request, response):
        for key, cookie in request.cookie_jar.all().items():
            cookie.value = request.app.make("sign").sign(cookie.value)

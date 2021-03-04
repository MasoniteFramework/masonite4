class EncryptCookies:
    def before(self, request, response):
        for key, cookie in request.cookie_jar.all().items():
            try:
                cookie.value = request.app.make("sign").unsign(cookie.value)
            except:
                cookie.value = cookie.value

        return request

    def after(self, request, response):
        for key, cookie in request.cookie_jar.all().items():
            cookie.value = request.app.make("sign").sign(cookie.value)

        return request

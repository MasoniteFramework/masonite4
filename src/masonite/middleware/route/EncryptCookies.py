from ...exceptions import InvalidToken


class EncryptCookies:
    def before(self, request, response):
        invalid_cookies = []
        for key, cookie in request.cookie_jar.all().items():
            try:
                cookie.value = request.app.make("sign").unsign(cookie.value)
            except InvalidToken:
                pass
                invalid_cookies.append(key)

        # self.delete_invalid_cookies(request, invalid_cookies)
        return request

    def after(self, request, response):
        invalid_cookies = []
        for key, cookie in request.cookie_jar.all().items():
            try:
                cookie.value = request.app.make("sign").sign(cookie.value)
            except InvalidToken:
                invalid_cookies.append(key)

        self.delete_invalid_cookies(request, invalid_cookies)
        return request

    def delete_invalid_cookies(self, request, invalid_cookies):
        for cookie in invalid_cookies:
            request.delete_cookie(cookie)

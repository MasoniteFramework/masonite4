class HttpTestResponse:
    def __init__(self, application, request, response, route):
        self.application = application
        self.request = request
        self.response = response
        self.route = route
        self.content = None
        self.status = None
        self.get_response()

    def get_response(self):
        self.content = self.response.get_response_content()
        return self

    def assertContains(self, content):
        assert content in str(self.content), f"{content} not found."
        return self

    def assertNotContains(self, content):
        assert content not in str(self.content)
        return self

    def assertContainsInOrder(self, *content):
        response_content = str(self.content)
        index = 0
        for content_string in content:
            found_at_index = response_content.find(content_string, index)
            assert found_at_index != -1
            index = found_at_index + len(content_string)
        return self

    def assertIsNamed(self, name):
        assert (
            self.route.get_name() == name
        ), f"Route name is {self.route.get_name()}. Asserted {name}"
        return self

    def assertIsNotNamed(self, name=None):
        if name is None:
            assert self.route.name is None, "Route has a name: {}".format(
                self.route.name
            )
        else:
            assert (
                self.route.get_name() != name
            ), f"Route name {self.route.get_name()} matches expected {name}"
        return self

    def assertIsStatus(self, status):
        assert self.response.is_status(status), f"Status is {self.response.get_status_code()}. Asserted {status}"
        return self

    def assertNotFound(self):
        return self.assertIsStatus(404)

    def assertOk(self):
        return self.assertIsStatus(200)

    def assertCreated(self):
        return self.assertIsStatus(201)

    def assertSuccessful(self):
        assert 200 <= self.response.get_status_code() < 300
        return self

    def assertNoContent(self, status=204):
        assert not str(self.response.content)
        return self.assertIsStatus(status)

    def assertUnauthorized(self):
        return self.assertIsStatus(401)

    def assertForbidden(self):
        return self.assertIsStatus(403)

    def assertHasHeader(self, name, value=None):
        header_value = self.response.header(name)
        assert header_value
        if value:
            assert value == header_value

    def assertHeaderMissing(self, name):
        assert not self.response.header(name)

    def assertLocation(self, location):
        return self.assertHasHeader("Location", location)

    def assertRedirect(self, url=None, name=None, params={}):
        # we could assert 301 or 302 code => what if user uses another status code in redirect()
        # here we are sure
        assert str(self.content) == "Redirecting ..."
        if url:
            self.assertLocation(url)
        elif name:
            url = self.response._get_url_from_route_name(name, params)
            self.assertLocation(url)
        return self

    def assertCookie(self, name, value=None):
        assert self.request.cookie_jar.exists(name)
        if value is not None:
            assert self.request.cookie_jar.get(name).value == value
        return self

    def assertPlainCookie(self, name):
        assert self.request.cookie_jar.exists(name)
        assert not self.request.cookie_jar.get(name).secure
        return self

    def assertCookieExpired(self, name):
        self.assertCookie(name)
        assert self.request.cookie_jar.is_expired(name)
        return self

    def assertCookieNotExpired(self, name):
        return not self.assertCookieExpired(name)

    def assertCookieMissing(self, name):
        assert not self.request.cookie_jar.exists(name)
        return self

    def assertSessionHas(self, key, value=None):
        # how to get session ?
        session = None
        session_value = session.get(key)
        assert session_value
        if value is not None:
            assert session_value == value
        return self

    def assertSessionMissing(self, key):
        # how to get session ?
        session = None
        assert not session.get(key)
        return self
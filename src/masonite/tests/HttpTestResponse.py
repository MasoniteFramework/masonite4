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

    def assertSuccessful(self):
        assert 200 <= self.response.get_status_code() < 300
        return self

    def assertUnauthorized(self):
        return self.assertIsStatus(401)

    def assertHasHeader(self, name, value=None):
        assert self.response.hasHeader(name, value)

    def assertHeaderMissing(self, name):
        assert not self.response.header(name)

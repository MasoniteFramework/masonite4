class HttpTestResponse:
    def __init__(self, application, route):
        self.application = application
        self.route = route
        self.content = None
        self.status = None
        self.get_response()

    def get_response(self):
        self.content = self.route.get_response(self.application)
        return self

    def assertContains(self, content):
        assert content in self.content
        return self

    def assertNotContains(self, content):
        assert content not in self.content
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

    def assertNotFound(self):
        return self.assertIsStatus(404)

    def assertIsStatus(self, status):
        pass

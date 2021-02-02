class HttpTestResponse:
    def __init__(self, application, route):
        self.application = application
        self.route = route
        self.content = None
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

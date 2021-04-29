from src.masonite.tests import TestCase


class TestHttpRequests(TestCase):
    def test_csrf_request(self):
        self.withoutCsrf()
        return self.post("/").assertContains("welcome")

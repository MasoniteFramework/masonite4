from tests import TestCase


class TestTesting(TestCase):
    def setUp(self):
        super().setUp()

    def test_can_get_route(self):
        self.get("/").assertContains("welcome")
        self.get("/").assertNotContains("welcome1")

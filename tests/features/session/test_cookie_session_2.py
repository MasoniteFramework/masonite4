from tests import TestCase


class TestCookieSession(TestCase):
    def test_can_start_session(self):
        request = self.make_request()
        session = self.application.make("session")
        request.cookie("s_hello", "test")
        session.start()
        self.assertEqual(session.get("hello"), "test")

    def test_can_set_and_get_session(self):
        self.make_request()
        session = self.application.make("session")
        session.start()
        session.set("key1", "test1")
        self.assertEqual(session.get("key1"), "test1")

    def test_can_save_session(self):
        self.make_request()
        response = self.make_response()
        session = self.application.make("session")
        session.start()
        session.set("key1", "test1")
        session.save()
        self.assertEqual(response.cookie("s_key1"), "test1")

    def test_can_delete_session(self):
        request = self.make_request()
        response = self.make_response()
        session = self.application.make("session")
        request.cookie("s_key", "test")
        session.start()

        self.assertEqual(session.get("key"), "test")

        session.delete("key")
        self.assertEqual(session.get("key"), None)

        session.save()
        self.assertEqual(response.cookie("s_key"), None)
        self.assertTrue("s_key" in response.cookie_jar.deleted_cookies)

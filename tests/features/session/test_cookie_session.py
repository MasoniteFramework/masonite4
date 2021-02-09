from tests import TestCase


class TestCookieSession(TestCase):
    def test_can_set_session(self):
        self.make_request()
        session = self.application.make("session").driver("cookie")

        session.set("key", "value")
        self.assertEqual(session.get("key"), "value")

    def test_can_set_session_flash(self):
        self.make_request()
        session = self.application.make("session").driver("cookie")

        session.flash("key", "value")
        self.assertEqual(session.get("key"), "value")

        self.assertEqual(session.get_flashed_messages(), {"key": "value"})
        self.assertFalse(session.get("key"))

    def test_can_set_session_delete(self):
        self.make_request()
        session = self.application.make("session").driver("cookie")

        session.set("key", "value")
        session.delete("key")

        self.assertFalse(session.get("key"))

    def test_can_get_errors(self):
        self.make_request()
        session = self.application.make("session").driver("cookie")
        session.flash("errors", {"email": ["Your email is not available"]})
        self.assertEqual(session.get_error_messages(), ["Your email is not available"])

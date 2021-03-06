from src.masonite.tests import TestCase
from src.masonite.utils.helpers import generate_wsgi
from src.masonite.foundation import Application
import os
from src.masonite.response import Response
from src.masonite.routes import RouteCapsule, Route


class TestResponseRedirect(TestCase):
    def setUp(self):
        application = Application(os.getcwd())
        application.bind("router", RouteCapsule(Route.get("/", None).name("home")))
        self.response = Response(application)

    def test_redirect(self):
        self.response.redirect("/")
        self.assertEqual(self.response.get_status(), 302)
        self.assertEqual(self.response.header_bag.get("Location").value, "/")

    def test_redirect_to_route_named_route(self):
        self.response.redirect(name="home")
        self.assertEqual(self.response.get_status(), 302)
        self.assertEqual(self.response.header_bag.get("Location").value, "/")

    def test_redirect_to_url(self):
        self.response.redirect(url="/login")
        self.assertEqual(self.response.get_status(), 302)
        self.assertEqual(self.response.header_bag.get("Location").value, "/login")

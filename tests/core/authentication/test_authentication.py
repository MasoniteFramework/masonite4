from tests import TestCase
from src.masonite.foundation import Application
import os
from masoniteorm.models import Model
from src.masonite.auth import Authenticates
from src.masonite.auth import Auth
from src.masonite.auth.guards import WebGuard


class User(Model, Authenticates):
    pass


class TestAuthentication(TestCase):
    def setUp(self):
        super().setUp()
        auth = Auth(self.application).set_authentication_model(User())
        auth.set_guard("web", WebGuard(self.application))
        self.application.bind("auth", auth)

    def test_attempt(self):
        user = User.find(1)
        self.assertTrue(user.attempt("idmann509@gmail.com", "secret"))
        self.assertFalse(user.attempt("idmann509@gmail.com", "secret1"))

    def test_auth_class_registers_cookie(self):
        self.make_request()
        self.application.make("auth").guard("web").attempt(
            "idmann509@gmail.com", "secret"
        )
        self.assertTrue(self.application.make("request").cookie("token"))

    def test_logout(self):
        self.make_request()

        self.application.make("auth").guard("web").attempt(
            "idmann509@gmail.com", "secret"
        )

        self.assertTrue(self.application.make("request").cookie("token"))

        self.application.make("auth").guard("web").logout()
        self.assertFalse(self.application.make("request").cookie("token"))

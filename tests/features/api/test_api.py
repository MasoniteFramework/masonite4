from tests import TestCase
from src.masonite.utils.helpers import random_string
from tests.integrations.app.User import User


class TestAPI(TestCase):
    def test_api_token(self):
        user = User.find(1)
        response = (
            self.get("/protected", {"api_token": "wrong"})
            .assertIsStatus(401)
            .assertContains("not authorized")
        )

        response = (
            self.get("/protected", {"api_token": user.api_token})
            .assertOk()
            .assertContains("authorized")
        )

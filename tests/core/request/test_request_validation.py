from tests import TestCase
from src.masonite.routes import Route


class TestRequestValidation(TestCase):
    def setUp(self):
        super().setUp()
        self.setRoutes(
            Route.get("/validate", "WelcomeController@validate").name("validate"),
            Route.get(
                "/validate-bag", "WelcomeController@validate_with_specific_bag"
            ).name("validate-bag"),
            Route.get("/validate-manually", "WelcomeController@validate_manually").name(
                "validate-manually"
            ),
        )

    # integration test with controller
    def test_request_validate(self):
        self.get("/validate").assertSessionHasErrors()

    def test_request_validate_with_bag(self):
        self.get("/validate-bag").assertSessionHasErrors(
            ["users-errors"]
        ).assertRedirect()

    def test_manual_validation_request(self):
        self.get("/validate-manually").assertSessionHasErrors().assertRedirect()

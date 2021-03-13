from tests import TestCase

from src.masonite.utils.location import (
    view_path,
    controller_path,
    seeds_path,
    migrations_path,
    config_path,
)


class TestLocation(TestCase):
    def test_view_path(self):
        location = view_path("app.html")
        self.assertTrue(location.endswith("tests/integrations/templates/app.html"))
        location = view_path("account/app.html")
        self.assertTrue(
            location.endswith("tests/integrations/templates/account/app.html")
        )
        location = view_path("account/app.html", absolute=False)
        self.assertEqual("tests/integrations/templates/account/app.html", location)

    def test_controller_path(self):
        location = controller_path("MyController.py")
        self.assertTrue(
            location.endswith("tests/integrations/controllers/MyController.py")
        )
        location = controller_path("account/MyController.py")
        self.assertTrue(
            location.endswith("tests/integrations/controllers/account/MyController.py")
        )
        location = controller_path("MyController.py", absolute=False)
        self.assertEqual("tests/integrations/controllers/MyController.py", location)

    def test_config_path(self):
        location = config_path("app.py")
        self.assertTrue(location.endswith("tests/integrations/config/app.py"))
        location = config_path("package/base.py")
        self.assertTrue(location.endswith("tests/integrations/config/package/base.py"))
        location = config_path("app.py", absolute=False)
        self.assertEqual("tests/integrations/config/app.py", location)

    def test_migrations_path(self):
        location = migrations_path("create_users_table.py")
        self.assertTrue(
            location.endswith(
                "tests/integrations/databases/migrations/create_users_table.py"
            )
        )
        location = migrations_path("package/create_team_table.py")
        self.assertTrue(
            location.endswith(
                "tests/integrations/databases/migrations/package/create_team_table.py"
            )
        )
        location = migrations_path("create_users_table.py", absolute=False)
        self.assertEqual(
            "tests/integrations/databases/migrations/create_users_table.py", location
        )

    def test_seeds_path(self):
        location = seeds_path("create_users.py")
        self.assertTrue(
            location.endswith("tests/integrations/databases/seeds/create_users.py")
        )
        location = seeds_path("package/create_teams.py")
        self.assertTrue(
            location.endswith(
                "tests/integrations/databases/seeds/package/create_teams.py"
            )
        )
        location = seeds_path("create_users.py", absolute=False)
        self.assertEqual("tests/integrations/databases/seeds/create_users.py", location)

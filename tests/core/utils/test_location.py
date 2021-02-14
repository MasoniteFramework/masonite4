from tests import TestCase

from src.masonite.utils.location import view_path, controller_path


class TestLocation(TestCase):
    def test_view_path(self):
        location = view_path("app.html")
        self.assertTrue(location.endswith("tests/integrations/templates/app.html"))
        location = view_path("account/app.html")
        self.assertTrue(location.endswith("tests/integrations/templates/account/app.html"))
        location = view_path("account/app.html", absolute=False)
        self.assertEqual("tests/integrations/templates/account/app.html", location)

    def test_controller_path(self):
        location = controller_path("MyController.py")
        self.assertTrue(location.endswith("tests/integrations/controllers/MyController.py"))
        location = controller_path("account/MyController.py")
        self.assertTrue(location.endswith("tests/integrations/controllers/account/MyController.py"))
        location = controller_path("MyController.py", absolute=False)
        self.assertEqual("tests/integrations/controllers/MyController.py", location)
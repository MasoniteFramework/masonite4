from src.masonite.tests import TestCase
from src.masonite.app import Application
import os


class TestAppApplication(TestCase):
    def test_initialize_application(self):
        app = Application(os.getcwd())
        self.assertTrue(app)

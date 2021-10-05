from tests import TestCase

from src.masonite.utils.str import random_string


class TestStringsUtils(TestCase):
    def test_random_string(self):
        self.assertEqual(len(random_string()), 4)
        self.assertEqual(len(random_string(10)), 10)
        self.assertIsInstance(random_string(5), str)
        self.assertNotEqual(random_string(), random_string())

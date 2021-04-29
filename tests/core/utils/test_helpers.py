from src.masonite.tests import TestCase

from src.masonite.utils import optional


class User:

    my_attr = 3

    def my_method(self):
        return 4


class TestHelpers(TestCase):
    def test_optional(self):
        user = User()
        self.assertEqual(optional(user).my_attr, 3)
        self.assertEqual(optional(user).my_method(), 4)
        self.assertEqual(optional(user).non_existing_attr, None)
        self.assertEqual(optional(user).non_existing_method(), None)

        self.assertEqual(optional(user, default=0).non_existing_attr, 0)
        self.assertEqual(optional(user, default=0).non_existing_method(), 0)

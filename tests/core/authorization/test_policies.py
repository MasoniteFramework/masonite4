from tests import TestCase
from masoniteorm.models import Model

from tests.integrations.policies.PostPolicy import PostPolicy


class User(Model):
    """User Model"""

    __fillable__ = ["name", "email", "password"]


class Post(Model):
    __fillable__ = ["user_id", "name"]


class TestGate(TestCase):
    def setUp(self):
        super().setUp()
        self.gate = self.application.make("gate")
        self.make_request()

    def tearDown(self):
        super().tearDown()
        self.gate.policies = {}
        # self.gate.permissions = {}
        # self.gate.before_callbacks = []
        # self.gate.after_callbacks = []

    def test_can_register_policies(self):
        self.gate.register_policies([(Post, PostPolicy)])
        self.assertEqual(self.gate.policies[Post], PostPolicy)

    def test_using_policies_with_argument(self):
        self.gate.register_policies([(Post, PostPolicy)])
        post = Post()
        post.user_id = 1
        # authenticates user 1
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")
        self.assertTrue(self.gate.allows("update", post))

    def test_using_policies_without_argument(self):
        self.gate.register_policies([(Post, PostPolicy)])
        # authenticates user 1
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")

        self.assertTrue(self.gate.allows("create", Post))

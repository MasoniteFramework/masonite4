from src.masonite.middleware import MiddlewareCapsule
import os
from tests import TestCase


class MockMiddleware:
    pass


class TestMiddleware(TestCase):
    def test_can_create_capsule(self):
        capsule = MiddlewareCapsule()

    def test_can_add_middleware(self):
        capsule = MiddlewareCapsule()
        capsule.add({"mock": MockMiddleware})
        capsule.add([MockMiddleware])

        self.assertTrue(len(capsule.route_middleware) == 1)
        self.assertTrue(len(capsule.http_middleware) == 1)

    def test_can_add_and_remove_middleware(self):
        capsule = MiddlewareCapsule()
        capsule.add({"mock": MockMiddleware})
        capsule.add([MockMiddleware])
        capsule.remove(MockMiddleware)

        self.assertTrue(len(capsule.route_middleware) == 1)
        self.assertTrue(len(capsule.http_middleware) == 0)

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

    def test_can_get_multiple_middleware(self):
        capsule = MiddlewareCapsule()
        capsule.add(
            {
                "mock": MockMiddleware,
                "mock1": MockMiddleware,
                "mock2": MockMiddleware,
                "mock3": [MockMiddleware, MockMiddleware],
            }
        )
        capsule.add([MockMiddleware])
        capsule.remove(MockMiddleware)

        self.assertTrue(
            len(capsule.get_route_middleware(["mock", "mock1", "mock2"])) == 3
        )
        self.assertTrue(
            len(capsule.get_route_middleware(["mock", "mock1", "mock2", "mock3"])) == 5
        )

    def test_can_parse_middleware_arguments(self):
        capsule = MiddlewareCapsule()
        capsule.add(
            {
                "mock": MockMiddleware,
            }
        )
        capsule.add([MockMiddleware])
        capsule.remove(MockMiddleware)
        middleware, args = capsule.get_route_middleware(["mock:arg1,arg2"])[0]
        assert middleware == MockMiddleware
        assert args == ["arg1", "arg2"]

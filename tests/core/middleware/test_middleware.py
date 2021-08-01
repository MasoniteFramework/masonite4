from src.masonite.middleware import MiddlewareCapsule
import os
from tests import TestCase


class MockMiddleware:
    def before(self, request, response, arg1):
        return request

    def after(self, request, response):

        return request


class TestMiddleware(TestCase):
    def test_can_create_capsule(self):
        capsule = MiddlewareCapsule()
        self.assertTrue(capsule)

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

    def test_can_run_middleware(self):
        request = self.make_request()
        response = self.make_response()
        capsule = MiddlewareCapsule()
        capsule.add(
            {
                "mock": MockMiddleware,
            }
        )

        capsule.run_route_middleware(["mock:arg1"], request, response)

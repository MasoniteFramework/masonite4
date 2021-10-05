import json
import io
import unittest
import pendulum

from ..routes import Router, Route
from .HttpTestResponse import HttpTestResponse
from ..foundation.response_handler import testcase_handler
from ..utils.http import generate_wsgi
from ..request import Request
from ..response import Response
from ..environment import LoadEnvironment
from .TestCommand import TestCommand


class TestCase(unittest.TestCase):
    def setUp(self):
        LoadEnvironment("testing")
        from wsgi import application

        self.application = application
        self.original_class_mocks = {}
        self._test_cookies = {}
        self._test_headers = {}
        if hasattr(self, "startTestRun"):
            self.startTestRun()
        self.withoutCsrf()

    def tearDown(self):
        if hasattr(self, "stopTestRun"):
            self.stopTestRun()

    def setRoutes(self, *routes):
        self.application.make("router").set(Route.group(*routes, middleware=["web"]))
        return self

    def addRoutes(self, *routes):
        self.application.make("router").add(Route.group(*routes, middleware=["web"]))
        return self

    def withCsrf(self):
        self._csrf = True
        return self

    def withoutCsrf(self):
        self._csrf = False
        return self

    def get(self, route, data=None):
        return self.fetch(route, data, method="GET")

    def post(self, route, data=None):
        return self.fetch(route, data, method="POST")

    def put(self, route, data=None):
        return self.fetch(route, data, method="PUT")

    def patch(self, route, data=None):
        return self.fetch(route, data, method="PATCH")

    def make_request(self, data={}):
        request = Request(generate_wsgi(data))
        request.app = self.application

        self.application.bind("request", request)
        return request

    def make_response(self, data={}):
        request = Response(generate_wsgi(data))
        request.app = self.application

        self.application.bind("response", request)
        return request

    def fetch(self, route, data=None, method=None):
        if data is None:
            data = {}
        if not self._csrf:
            token = self.application.make("sign").sign("cookie")
            data.update({"__token": "cookie"})
            wsgi_request = generate_wsgi(
                {
                    "HTTP_COOKIE": f"SESSID={token}; csrf_token={token}",
                    "CONTENT_LENGTH": len(str(json.dumps(data))),
                    "REQUEST_METHOD": method,
                    "PATH_INFO": route,
                    "wsgi.input": io.BytesIO(bytes(json.dumps(data), "utf-8")),
                }
            )
        else:
            wsgi_request = generate_wsgi(
                {
                    "CONTENT_LENGTH": len(str(json.dumps(data))),
                    "REQUEST_METHOD": method,
                    "PATH_INFO": route,
                    "wsgi.input": io.BytesIO(bytes(json.dumps(data), "utf-8")),
                }
            )

        request, response = testcase_handler(
            self.application,
            wsgi_request,
            self.mock_start_response,
            exception_handling=False,
        )
        # add eventual cookies added inside the test (not encrypted to be able to assert value ?)
        for name, value in self._test_cookies.items():
            request.cookie(name, value)
        # add eventual headers added inside the test
        for name, value in self._test_headers.items():
            request.header(name, value)

        route = self.application.make("router").find(route, method)
        if route:
            return self.application.make("tests.response").build(
                self.application, request, response, route
            )
        raise Exception(f"No route found for {route}")

    def mock_start_response(self, *args, **kwargs):
        pass

    def craft(self, command, arguments_str=""):
        """Run a given command in tests and obtain a TestCommand instance to assert command
        outputs.
        self.craft("controller", "Welcome").assertSuccess()
        """
        return TestCommand(self.application).run(command, arguments_str)

    def fake(self, binding):
        """Mock a service with its mocked implementation or with a given custom
        one."""

        # save original first
        self.original_class_mocks.update(
            {binding: self.application.make(binding, self.application)}
        )
        # mock by overriding with mocked version
        mock = self.application.make(f"mock.{binding}", self.application)
        self.application.bind(binding, mock)
        return mock

    def withCookies(self, cookies_dict):
        self._test_cookies = cookies_dict
        return self

    def withHeaders(self, headers_dict):
        self._test_headers = headers_dict
        return self

    def actingAs(self, user):
        self.make_request()
        self.application.make("auth").guard("web").login_by_id(
            user.get_primary_key_value()
        )

    def restore(self, binding):
        """Restore the service previously mocked to the original one."""
        original = self.original_class_mocks.get(binding)
        self.application.bind(binding, original)

    def fakeTime(self, pendulum_datetime):
        """Set a given pendulum instance to be returned when a "now" (or "today", "tomorrow",
        "yesterday") instance is created. It's really useful during tests to check
        timestamps logic."""
        pendulum.set_test_now(pendulum_datetime)

    def fakeTimeTomorrow(self):
        """Set the mocked time as tomorrow."""
        self.fakeTime(pendulum.tomorrow())

    def fakeTimeYesterday(self):
        """Set the mocked time as yesterday."""
        self.fakeTime(pendulum.yesterday())

    def fakeTimeInFuture(self, offset, unit="days"):
        """Set the mocked time as an offset of days in the future. Unit can be specified
        among pendulum units: seconds, minutes, hours, days, weeks, months, years."""
        self.restoreTime()
        datetime = pendulum.now().add(**{unit: offset})
        self.fakeTime(datetime)

    def fakeTimeInPast(self, offset, unit="days"):
        """Set the mocked time as an offset of days in the past. Unit can be specified
        among pendulum units: seconds, minutes, hours, days, weeks, months, years."""
        self.restoreTime()
        datetime = pendulum.now().subtract(**{unit: offset})
        self.fakeTime(datetime)

    def restoreTime(self):
        """Restore time to correct one, so that pendulum new "now" instance are corrects.
        This method will be typically called in tearDown() method of a test class."""
        # this will clear the mock
        pendulum.set_test_now()

    def assertDatabaseCount(self, table, count):
        self.assertEqual(self.application.make("builder").table(table).count(), count)

    def assertDatabaseHas(self, table, query_dict):
        self.assertGreaterEqual(
            self.application.make("builder").table(table).where(query_dict).count(), 1
        )

    def assertDatabaseMissing(self, table, query_dict):
        self.assertEqual(
            self.application.make("builder").table(table).where(query_dict).count(), 0
        )

    def assertDeleted(self, instance):
        self.assertFalse(
            self.application.make("builder")
            .table(instance.get_table_name())
            .where(instance.get_primary_key(), instance.get_primary_key_value())
            .get()
        )

    def assertSoftDeleted(self, instance):
        deleted_at_column = instance.get_deleted_at_column()
        self.assertTrue(
            self.application.make("builder")
            .table(instance.get_table_name())
            .where(instance.get_primary_key(), instance.get_primary_key_value())
            .where_not_null(deleted_at_column)
            .get()
        )

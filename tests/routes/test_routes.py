from unittest import TestCase
from src.masonite.routes import Route, RouteCapsule


class TestRoutes(TestCase):
    def test_can_add_routes(self):
        Route.get("/home", "TestController")
        Route.post("/login", "TestController")
        self.assertEqual(len(Route().routes), 2)

    def test_can_find_route(self):
        router = RouteCapsule(Route.get("/home", "TestController"))

        route = router.find("/home/", "GET")
        self.assertTrue(route)

    def test_can_find_route_with_parameter(self):
        router = RouteCapsule(Route.get("/home/@id", "TestController"))

        route = router.find("/home/1", "GET")
        self.assertTrue(route)

    def test_can_find_route_optional_params(self):
        router = RouteCapsule(Route.get("/home/?id", "TestController"))

        route = router.find("/home/1", "GET")
        self.assertTrue(route)
        route = router.find("/home", "GET")
        self.assertTrue(route)

    def test_can_find_route_compiler(self):
        router = RouteCapsule(Route.get("/route/@id:int", "TestController"))

        route = router.find("/route/1", "GET")
        self.assertTrue(route)
        route = router.find("/route/string", "GET")
        self.assertFalse(route)

    def test_can_make_route_group(self):
        router = RouteCapsule(
            Route.group(
                Route.get("/group", "TestController@show"),
                Route.post("/login", "TestController@show"),
                prefix="/testing",
            )
        )

        route = router.find("/testing/group", "GET")
        self.assertTrue(route)

    def test_group_naming(self):
        router = RouteCapsule(
            Route.group(
                Route.get("/group", "TestController@show").name(".index"),
                Route.post("/login", "TestController@show").name(".index"),
                prefix="/testing",
                name="dashboard",
            )
        )

        route = router.find_by_name("dashboard.index")
        self.assertTrue(route)

    def test_compile_year(self):
        Route.compile("year", r"[0-9]{4}")
        router = RouteCapsule(Route.get("/year/@date:year", "TestController@show"))

        route = router.find("/year/2005", "GET")
        self.assertTrue(route)

    def test_find_by_name(self):
        router = RouteCapsule(
            Route.get("/getname", "TestController@show").name("testname")
        )

        route = router.find_by_name("testname")
        self.assertTrue(route)

    def test_extract_parameters(self):
        router = RouteCapsule(
            Route.get("/params/@id", "TestController@show").name("testparam")
        )

        route = router.find_by_name("testparam")
        self.assertEqual(route.extract_parameters("/params/2")["id"], "2")

    def test_domain(self):
        router = RouteCapsule(
            Route.get("/domain/@id", "TestController@show").domain("sub")
        )

        route = router.find("/domain/2", "get")
        self.assertIsNone(route)

        route = router.find("/domain/2", "get", "sub")
        self.assertTrue(route)

from .Provider import Provider
from ..routes import RouteCapsule, Route
from ..pipeline import Pipeline
from ..middleware.route import VerifyCsrfToken


class RouteProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        # Register the routes?
        Route.set_controller_module_location(
            self.application.make("controller.location")
        )
        self.application.bind(
            "router",
            RouteCapsule(
                Route.get("/", "WelcomeController@show"),
                Route.get("/test", "WelcomeController@test"),
                Route.get("/view", "WelcomeController@view"),
            ),
        )

    def boot(self):
        router = self.application.make("router")
        request = self.application.make("request")
        response = self.application.make("response")

        route = router.find(request.get_path(), request.get_request_method())

        # Run before middleware

        if route:
            Pipeline(request, response).through([VerifyCsrfToken], handler="before")

            response.view(route.get_response(self.application))

            Pipeline(request, response).through([VerifyCsrfToken], handler="after")
        else:
            raise Exception(f"NO route found for {request.get_path()}")

from .Provider import Provider
from ..routes import Router, Route
from ..pipeline import Pipeline

# from ..middleware.route import VerifyCsrfToken
import pydoc


class RouteProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        # Register the routes?
        Route.set_controller_module_location(
            self.application.make("controller.location")
        )

    def boot(self):
        router = self.application.make("router")
        request = self.application.make("request")
        response = self.application.make("response")

        route = router.find(
            request.get_path(), request.get_request_method(), request.get_subdomain()
        )

        # Run before middleware

        Pipeline(request, response).through(
            self.application.make("middleware").get_http_middleware(),
            handler="before",
        )
        if route:
            request.load_params(route.extract_parameters(request.get_path()))
            self.application.make("middleware").run_route_middleware(
                route.list_middleware, request, response, callback="before"
            )
            exception = None

            try:
                response.view(route.get_response(self.application))
            except Exception as e:
                exception = e
                self.application.make("middleware").run_route_middleware(
                    route.list_middleware, request, response, callback="after"
                )
                if exception:
                    raise exception

            self.application.make("middleware").run_route_middleware(
                route.list_middleware, request, response, callback="after"
            )

        else:
            response.view("route not found", status=404)

        Pipeline(request, response).through(
            self.application.make("middleware").get_http_middleware(),
            handler="after",
        )

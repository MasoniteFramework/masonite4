from .Provider import Provider
from ..routes import RouteCapsule, Route
from ..pipeline import Pipeline

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

        route = router.find(request.get_path(), request.get_request_method())

        # Run before middleware
        if route:
            request.url_params = route.extract_parameters(request.get_path())
            pipe = Pipeline(request, response).through(
                (
                    self.application.make("middleware").get_http_middleware()
                    + self.application.make("middleware").get_route_middleware(
                        route.get_middleware()
                    )
                ),
                handler="before",
            )

            print('before pipe')

            if pipe:
                response.view(route.get_response(self.application))

            print('after pipe')
            Pipeline(request, response).through(
                (
                    self.application.make("middleware").get_http_middleware()
                    + self.application.make("middleware").get_route_middleware(
                        route.get_middleware()
                    )
                ),
                handler="after",
            )
        else:
            response.view("route not found", status=404)

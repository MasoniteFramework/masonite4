from .Provider import Provider
from exceptionite.errors import Handler, StackOverflowIntegration, SolutionsIntegration

# from exceptionite.errors
# from


class MasoniteHandler:
    def __init__(self, application):
        self.application = application

    def load_exception(self, e):
        response = self.application.make("response")
        request = self.application.make("request")
        handler = Handler(e)
        # handler.integrate(StackOverflowIntegration())
        handler.integrate(SolutionsIntegration())
        handler.context(
            {
                "WSGI": {
                    "Path": request.get_path(),
                    "Input": request.input_bag.all_as_values() or None,
                    # 'Parameters': request.url_params,
                    "Request Method": request.get_request_method(),
                },
                "Headers": {},
            }
        )

        return response.view(handler.render(), status=500)

    def get_headers(self, request):
        headers = {}
        for header, value in request.environ.items():
            if header.startswith("HTTP_"):
                headers.update({header: value})

        return headers


class ExceptionProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.bind("ExceptionHandler", MasoniteHandler(self.application))

    def boot(self):
        pass

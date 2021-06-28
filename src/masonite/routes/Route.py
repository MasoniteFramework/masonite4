from .HTTPRoute import HTTPRoute
from ..utils.helpers import flatten
from ..controllers import RedirectController


class Route:

    routes = []
    compilers = {
        "int": r"(\d+)",
        "integer": r"(\d+)",
        "string": r"([a-zA-Z]+)",
        "default": r"([\w.-]+)",
        "signed": r"([\w\-=]+)",
    }

    def __init__(self):
        pass

    @classmethod
    def get(self, url, controller, module_location=None, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=["get"],
            compilers=self.compilers,
            module_location=module_location or self.controller_module_location,
            **options
        )

    @classmethod
    def post(self, url, controller, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=["post"],
            compilers=self.compilers,
            module_location=self.controller_module_location,
            **options
        )

    @classmethod
    def put(self, url, controller, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=["put"],
            compilers=self.compilers,
            module_location=self.controller_module_location,
            **options
        )

    @classmethod
    def patch(self, url, controller, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=["patch"],
            compilers=self.compilers,
            module_location=self.controller_module_location,
            **options
        )

    @classmethod
    def delete(self, url, controller, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=["delete"],
            compilers=self.compilers,
            module_location=self.controller_module_location,
            **options
        )

    @classmethod
    def options(self, url, controller, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=["options"],
            compilers=self.compilers,
            module_location=self.controller_module_location,
            **options
        )

    @classmethod
    def default(self, url, controller, **options):
        return self

    @classmethod
    def redirect(self, url, new_url, **options):
        return HTTPRoute(
            url,
            RedirectController.redirect,
            request_method=["get"],
            compilers=self.compilers,
            module_location=self.controller_module_location,
            controller_bindings=[new_url, options.get("status", 302)],
            **options
        )

    @classmethod
    def permanent_redirect(self, url, new_url, **options):
        return HTTPRoute(
            url,
            RedirectController.redirect,
            request_method=["get"],
            compilers=self.compilers,
            module_location=self.controller_module_location,
            controller_bindings=[new_url, 301],
            **options
        )

    @classmethod
    def match(self, request_methods, url, controller, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=request_methods,
            compilers=self.compilers,
            module_location=self.controller_module_location,
            **options
        )

    @classmethod
    def group(self, *routes, **options):
        inner = []
        for route in flatten(routes):
            if options.get("prefix"):
                route.url = options.get("prefix") + route.url
                route.compile_route_to_regex()

            if options.get("name"):
                route._name = options.get("name") + route._name

            if options.get("domain"):
                route.domain(options.get("domain"))

            if options.get("middleware"):
                route.middleware(*options.get("middleware", []))

            inner.append(route)
        self.routes = inner
        return inner

    @classmethod
    def compile(self, key, to=""):
        self.compilers.update({key: to})
        return self

    @classmethod
    def set_controller_module_location(self, controller_location):
        self.controller_module_location = controller_location
        return self

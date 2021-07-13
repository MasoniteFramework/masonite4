from ..utils.helpers import flatten
from ..exceptions import RouteNotFoundException


class Router:
    def __init__(self, *routes, module_location=None):
        self.routes = flatten(routes)

    def find(self, path, request_method, subdomain=None):

        for route in self.routes:
            if route.match(path, request_method, subdomain=subdomain):
                return route

    def matches(self, path):
        for route in self.routes:
            if route.matches(path):
                return route

    def find_by_name(self, name):
        for route in self.routes:
            if route.match_name(name):
                return route

    def route(self, name, parameters={}):
        route = self.find_by_name(name)
        if route:
            return route.to_url(parameters)
        raise RouteNotFoundException(f"Could not find route with the name '{name}'")

    def set_controller_module_location(self, location):
        self.controller_module_location = location
        return self

    def add(self, *routes):
        self.routes.append(*routes)
        self.routes = flatten(self.routes)

    def set(self, *routes):
        self.routes = []
        self.routes.append(*routes)
        self.routes = flatten(self.routes)

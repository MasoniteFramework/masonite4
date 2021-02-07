from ..utils.helpers import flatten


class RouteCapsule:
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

    def set_controller_module_location(self, location):
        self.controller_module_location = location
        return self

    def add(self, *routes):
        self.routes.extend(routes)

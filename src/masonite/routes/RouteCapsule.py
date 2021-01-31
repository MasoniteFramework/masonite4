from ..utils.helpers import flatten_routes


class RouteCapsule:
    def __init__(self, *routes):
        self.routes = flatten_routes(routes)

    def find(self, path, request_method, subdomain=None):
        print(self.routes)
        for route in self.routes:
            if route.match(path, request_method, subdomain=subdomain):
                return route

    def matches(self, path):
        for route in self.routes:
            if route.matches(path):
                return route

    def find_by_name(self, name):
        for route in self.routes:
            print(route)
            if route.match_name(name):
                return route

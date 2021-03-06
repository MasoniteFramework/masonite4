class MiddlewareCapsule:
    def __init__(self):
        self.route_middleware = {}
        self.http_middleware = []

    def add(self, middleware):
        if isinstance(middleware, dict):
            self.route_middleware.update(middleware)

        if isinstance(middleware, list):
            self.http_middleware += middleware

        return self

    def remove(self, middleware):
        if middleware in self.route_middleware:
            self.route_middleware.pop(middleware)
        elif middleware in self.http_middleware:
            self.http_middleware.pop(self.http_middleware.index(middleware))
        return self

    def get_route_middleware(self, keys=None):
        middlewares = []
        if keys is None:
            return self.route_middleware

        if keys is None:
            keys = []

        for key in keys:
            found = self.route_middleware[key]
            if isinstance(found, list):
                middlewares += found
            else:
                middlewares += [found]
        return middlewares

    def get_http_middleware(self):
        return self.http_middleware

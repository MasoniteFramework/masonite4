class MiddlewareCapsule:
    def __init__(self):
        self.route_middleware = {}
        self.http_middleware = []

    def add(self, middleware):
        if isinstance(middleware, dict):
            self.route_middleware.update(middleware)

        if isinstance(middleware, list):
            self.http_middleware += middleware

    def remove(self, middleware):
        if middleware in self.route_middleware:
            self.route_middleware.pop(middleware)
        elif middleware in self.http_middleware:
            self.http_middleware.pop(self.http_middleware.index(middleware))

        return self

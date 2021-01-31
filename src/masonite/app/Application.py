class Application:
    def __init__(self, base_path=None):
        self.base_path = base_path
        self.storage_path = None
        self.routes = []

    def load_routes(self, routes):
        self.routes = routes

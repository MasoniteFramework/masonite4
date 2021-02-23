import builtins
from ..providers import Provider


class HelpersProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        builtins.resolve = self.application.resolve
        builtins.container = lambda: self.application

    def boot(self):
        request = self.application.make("request")
        self.application.make("view").share(
            {
                "request": lambda: request,
                "auth": request.user,
                "route": self.application.make("router").route,
                "cookie": request.cookie,
                # "url": lambda name, params={}: request.route(name, params, full=True),
            }
        )

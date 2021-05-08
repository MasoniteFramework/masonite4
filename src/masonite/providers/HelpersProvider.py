import builtins
from ..providers import Provider
from ..utils.helpers import AssetHelper, UrlHelper


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
                "cookie": request.cookie,
                "asset": AssetHelper(self.application).asset,
                "url": UrlHelper(self.application).url,
                "route": lambda name, params={}: (
                    self.application.make("base_url")
                    + self.application.make("router").route(name, params)
                ),
            }
        )

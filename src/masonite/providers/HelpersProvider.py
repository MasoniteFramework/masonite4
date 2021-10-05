import builtins
from ..providers import Provider
from ..utils.helpers import AssetHelper, UrlHelper
from markupsafe import Markup


class HelpersProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        builtins.resolve = self.application.resolve
        builtins.container = lambda: self.application
        self.application.bind("url", UrlHelper(self.application))

    def boot(self):
        request = self.application.make("request")
        self.application.make("view").share(
            {
                "request": lambda: request,
                "session": lambda: request.app.make("session"),
                "auth": request.user,
                "cookie": request.cookie,
                "back": lambda url=request.get_path(): (
                    Markup(f"<input type='hidden' name='__back' value='{url}' />")
                ),
                "asset": AssetHelper(self.application).asset,
                "url": UrlHelper(self.application).url,
                "route": lambda name, params={}: (
                    self.application.make("base_url")
                    + self.application.make("router").route(name, params)
                ),
            }
        )

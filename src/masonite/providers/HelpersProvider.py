import builtins
from ..providers import Provider
from ..helpers.urls import UrlsHelper
from markupsafe import Markup


class HelpersProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        builtins.resolve = self.application.resolve
        builtins.container = lambda: self.application
        self.application.bind("url", UrlsHelper(self.application))

    def boot(self):
        request = self.application.make("request")
        urls_helper = self.application.make("url")

        self.application.make("view").share(
            {
                "request": lambda: request,
                "session": lambda: request.app.make("session"),
                "auth": request.user,
                "cookie": request.cookie,
                "back": lambda url=request.get_path(): (
                    Markup(f"<input type='hidden' name='__back' value='{url}' />")
                ),
                "asset": urls_helper.asset,
                "url": urls_helper.url,
                "route": urls_helper.route,
            }
        )

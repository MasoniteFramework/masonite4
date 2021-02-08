from ..foundation import response_handler
from ..request import Request
from ..response import Response

from ..exception_handler import DD
from ..helpers.view_helpers import back, set_request_method, hidden, old
from ..helpers.sign import sign, unsign, decrypt, encrypt
from ..helpers import config, optional
from ..provider import ServiceProvider
from ..view import View
from ..request import Request
from ..managers import MailManager


class HelpersProvider:
    def __init__(self, application):
        self.application = application

    def register(self):
        builtins.view = self.application.make('view').render
        builtins.env = os.getenv
        builtins.resolve = self.application.resolve

    def boot(self):
        view.share(
            {
                "request": lambda: self.application.make('request'),
                "auth": request.user,
                # "route": request.route,
                "cookie": request.get_cookie,
                # "url": lambda name, params={}: request.route(name, params, full=True),
            }
        )

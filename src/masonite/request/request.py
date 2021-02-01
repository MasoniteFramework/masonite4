from ..cookies import CookieJar
from ..headers import HeaderBag
from ..input import InputBag


class Request:
    def __init__(self, environ):
        """Request class constructor.

        Initializes several properties and sets various methods
        depending on the environtment.

        Keyword Arguments:
            environ {dictionary} -- WSGI environ dictionary. (default: {None})
        """
        self.environ = environ
        self.cookie_jar = CookieJar()
        self.header_bag = HeaderBag()
        self.input_bag = InputBag()

    def load(self):
        self.cookie_jar.load(self.environ)
        self.header_bag.load(self.environ)
        self.input_bag.load(self.environ)

    def get_path(self):
        return self.environ.get("PATH_INFO")

    def get_request_method(self):
        return self.environ.get("REQUEST_METHOD")

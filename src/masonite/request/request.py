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
        self.load()

    def load(self):
        self.cookie_jar.load(self.environ["HTTP_COOKIE"])
        self.header_bag.load(self.environ)
        self.input_bag.load(self.environ)

    def get_path(self):
        return self.environ.get("PATH_INFO")

    def get_request_method(self):
        return self.environ.get("REQUEST_METHOD")

    def input(self, name, default=False, clean=False, quote=True):
        """Get a specific input value.

        Arguments:
            name {string} -- Key of the input data

        Keyword Arguments:
            default {string} -- Default value if input does not exist (default: {False})
            clean {bool} -- Whether or not the return value should be
                            cleaned (default: {True})

        Returns:
            string
        """
        name = str(name)

        return self.input_bag.get(name, default=default, clean=clean, quote=quote)

    def cookie(self, name, value=None):
        if value is None:
            return self.cookie_jar.get(name)
        else:
            return self.cookie_jar.add(name, value)

    def all(self):
        return self.input_bag.all()

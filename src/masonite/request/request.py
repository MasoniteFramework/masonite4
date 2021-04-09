from ..exceptions import ValidationException
from ..cookies import CookieJar
from ..headers import HeaderBag, Header
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
        self.cookie_jar.load(self.environ.get("HTTP_COOKIE", ""))
        self.header_bag.load(self.environ)
        self.input_bag.load(self.environ)

    def get_path(self):
        return self.environ.get("PATH_INFO")

    def get_request_method(self):
        return self.environ.get("REQUEST_METHOD")

    def input(self, name, default=False):
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

        return self.input_bag.get(name, default=default)

    def cookie(self, name, value=None):
        if value is None:
            cookie = self.cookie_jar.get(name)
            if not cookie:
                return
            return cookie.value

        return self.cookie_jar.add(name, value)

    def delete_cookie(self, name):
        self.cookie_jar.delete(name)
        return self

    def header(self, name, value=None):
        if value is None:
            return self.header_bag.get(name)
        else:
            return self.header_bag.add(Header(name, value))

    def all(self):
        return self.input_bag.all_as_values()

    def only(self, *inputs):
        return self.input_bag.only(*inputs)

    def is_not_safe(self):
        """Check if the current request is not a get request.

        Returns:
            bool
        """
        if not self.get_request_method() in ("GET", "OPTIONS", "HEAD"):
            return True

        return False

    def user(self):
        return self._user

    def set_user(self, user):
        self._user = user
        return self

    def remove_user(self):
        self._user = None
        return self

    def validate(self, *rules, bag=None):
        from wsgi import application

        validator = application.make("validator")
        validation_bag = validator.validate(self.all(), *rules)

        if validation_bag.any():
            raise ValidationException(validation_bag, bag)

        return validation_bag

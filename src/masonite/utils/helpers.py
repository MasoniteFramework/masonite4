def flatten(routes):
    """Flatten the grouped lists of lists into a single list.

    Arguments:
        routes {list} -- This can be a multi dementional list which can flatten all lists into a single list.

    Returns:
        list -- Returns the flatten list.
    """
    route_collection = []
    for route in routes:
        if isinstance(route, list):
            for r in flatten(route):
                route_collection.append(r)
        else:
            route_collection.append(route)

    return route_collection


"""Helper Functions for working with Status Codes."""


def response_statuses():
    return {
        100: "100 Continue",
        101: "101 Switching Protocol",
        102: "102 Processing",
        103: "Early Hints",
        200: "200 OK",
        201: "201 Created",
        202: "202 Accepted",
        203: "203 Non-Authoritative Information",
        204: "204 No Content",
        205: "205 Reset Content",
        206: "206 Partial Content",
        207: "207 Multi-Status",
        208: "208 Multi-Status",
        226: "226 IM Used",
        300: "300 Multiple Choice",
        301: "301 Moved Permanently",
        302: "302 Found",
        303: "303 See Other",
        304: "304 Not Modified",
        307: "307 Temporary Redirect",
        308: "308 Permanent Redirect",
        400: "400 Bad Request",
        401: "401 Unauthorized",
        402: "402 Payment Required",
        403: "403 Forbidden",
        404: "404 Not Found",
        405: "405 Method Not Allowed",
        406: "406 Not Acceptable",
        407: "407 Proxy Authentication Required",
        408: "408 Request Timeout",
        409: "409 Conflict",
        410: "410 Gone",
        411: "411 Length Required",
        412: "412 Precondition Failed",
        413: "413 Payload Too Large",
        414: "414 URI Too Long",
        415: "415 Unsupported Media Type",
        416: "416 Requested Range Not Satisfiable",
        417: "417 Expectation Failed",
        418: "418 I'm a teapot",
        421: "421 Misdirected Request",
        422: "422 Unprocessable Entity",
        423: "423 Locked",
        424: "424 Failed Dependency",
        425: "425 Too Early",
        426: "426 Upgrade Required",
        428: "428 Precondition Required",
        429: "429 Too Many Requests",
        431: "431 Request Header Fields Too Large",
        451: "451 Unavailable For Legal Reasons",
        500: "500 Internal Server Error",
        501: "501 Not Implemented",
        502: "502 Bad Gateway",
        503: "503 Service Unavailable",
        504: "504 Gateway Timeout",
        505: "505 HTTP Version Not Supported",
        506: "506 Variant Also Negotiates",
        507: "507 Insufficient Storage",
        508: "508 Loop Detected",
        510: "510 Not Extended",
        511: "511 Network Authentication Required",
    }


"""Time Module."""


def cookie_expire_time(str_time):
    """Take a string like 1 month or 5 minutes and returns a pendulum instance.

    Arguments:
        str_time {string} -- Could be values like 1 second or 3 minutes

    Returns:
        pendulum -- Returns Pendulum instance
    """
    import pendulum

    if str_time != "expired":
        number = int(str_time.split(" ")[0])
        length = str_time.split(" ")[1]

        if length in ("second", "seconds"):
            # Sat, 06 Jun 2020 15:36:16 GMT
            return (
                pendulum.now("GMT")
                .add(seconds=number)
                .format("ddd, DD MMM YYYY H:mm:ss")
            )
        elif length in ("minute", "minutes"):
            return (
                pendulum.now("GMT")
                .add(minutes=number)
                .format("ddd, DD MMM YYYY H:mm:ss")
            )
        elif length in ("hour", "hours"):
            return (
                pendulum.now("GMT").add(hours=number).format("ddd, DD MMM YYYY H:mm:ss")
            )
        elif length in ("days", "days"):
            return (
                pendulum.now("GMT").add(days=number).format("ddd, DD MMM YYYY H:mm:ss")
            )
        elif length in ("week", "weeks"):
            return pendulum.now("GMT").add(weeks=1).format("ddd, DD MMM YYYY H:mm:ss")
        elif length in ("month", "months"):
            return (
                pendulum.now("GMT")
                .add(months=number)
                .format("ddd, DD MMM YYYY H:mm:ss")
            )
        elif length in ("year", "years"):
            return (
                pendulum.now("GMT").add(years=number).format("ddd, DD MMM YYYY H:mm:ss")
            )

        return None
    else:
        return pendulum.now("GMT").subtract(years=20).format("ddd, DD MMM YYYY H:mm:ss")


def parse_human_time(str_time):
    """Take a string like 1 month or 5 minutes and returns a pendulum instance.

    Arguments:
        str_time {string} -- Could be values like 1 second or 3 minutes

    Returns:
        pendulum -- Returns Pendulum instance
    """
    import pendulum

    if str_time == "now":
        return pendulum.now("GMT")

    if str_time != "expired":
        number = int(str_time.split(" ")[0])
        length = str_time.split(" ")[1]

        if length in ("second", "seconds"):
            return pendulum.now("GMT").add(seconds=number)
        elif length in ("minute", "minutes"):
            return pendulum.now("GMT").add(minutes=number)
        elif length in ("hour", "hours"):
            return pendulum.now("GMT").add(hours=number)
        elif length in ("days", "days"):
            return pendulum.now("GMT").add(days=number)
        elif length in ("week", "weeks"):
            return pendulum.now("GMT").add(weeks=1)
        elif length in ("month", "months"):
            return pendulum.now("GMT").add(months=number)
        elif length in ("year", "years"):
            return pendulum.now("GMT").add(years=number)

        return None
    else:
        return pendulum.now("GMT").subtract(years=20)


def generate_wsgi(wsgi=None):
    import io

    if wsgi is None:
        wsgi = {}
    data = {
        "wsgi.version": (1, 0),
        "wsgi.multithread": False,
        "wsgi.multiprocess": True,
        "wsgi.run_once": False,
        "wsgi.input": io.BytesIO(),
        "SERVER_SOFTWARE": "gunicorn/19.7.1",
        "REQUEST_METHOD": "GET",
        "QUERY_STRING": "application=Masonite",
        "RAW_URI": "/",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "HTTP_HOST": "127.0.0.1:8000",
        "HTTP_ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "HTTP_UPGRADE_INSECURE_REQUESTS": "1",
        "HTTP_COOKIE": "setcookie=value",
        "HTTP_USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7",
        "HTTP_ACCEPT_LANGUAGE": "en-us",
        "HTTP_ACCEPT_ENCODING": "gzip, deflate",
        "HTTP_CONNECTION": "keep-alive",
        "wsgi.url_scheme": "http",
        "REMOTE_ADDR": "127.0.0.1",
        "REMOTE_PORT": "62241",
        "SERVER_NAME": "127.0.0.1",
        "SERVER_PORT": "8000",
        "PATH_INFO": "/",
        "SCRIPT_NAME": "",
    }
    data.update(wsgi)
    return data


class Dot:
    def dot(self, search, dictionary, default=None):
        """The search string in dot notation to look into the dictionary for.

        Arguments:
            search {string} -- This should be a string in dot notation
                                like 'key.key.value'.
            dictionary {dict} -- A normal dictionary which will be searched using
                                the search string in dot notation.

        Keyword Arguments:
            default {string} -- The default value if nothing is found
                                in the dictionary. (default: {None})

        Returns:
            string -- Returns the value found the dictionary or the default
                        value specified above if nothing is found.
        """
        if "." not in search:
            if search == "":
                return dictionary
            try:
                return dictionary[search]
            except KeyError:
                return default

        searching = search.split(".")
        possible = None
        if "*" not in search:
            return self.flatten(dictionary).get(search, default)

        while searching:
            dic = dictionary
            for value in searching:
                if not dic:
                    if "*" in searching:
                        return []
                    return default

                if isinstance(dic, list):
                    try:
                        return collect(dic).pluck(searching[searching.index("*") + 1])
                    except KeyError:
                        return []

                if not isinstance(dic, dict):
                    return default

                dic = dic.get(value)

                if isinstance(dic, str) and dic.isnumeric():
                    continue

                if (
                    dic
                    and not isinstance(dic, int)
                    and hasattr(dic, "__len__")
                    and len(dic) == 1
                    and not isinstance(dic[list(dic)[0]], dict)
                ):
                    possible = dic

            if not isinstance(dic, dict):
                return dic

            del searching[-1]
        return possible

    def flatten(self, d, parent_key="", sep="."):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                items.append((new_key, v))
                items.extend(self.flatten(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for index, val in enumerate(v):
                    items.extend(
                        self.flatten({str(index): val}, new_key, sep=sep).items()
                    )
            else:
                items.append((new_key, v))

        return dict(items)

    def locate(self, search_path, default=""):
        """Locate the object from the given search path

        Arguments:
            search_path {string} -- A search path to fetch the object
                                    from like config.application.debug.

        Keyword Arguments:
            default {string} -- A default string if the search path is
                                not found (default: {''})

        Returns:
            any -- Could be a string, object or anything else that is fetched.
        """
        value = self.find(search_path, default)

        if isinstance(value, dict):
            return self.dict_dot(".".join(search_path.split(".")[3:]), value, default)

        if value is not None:
            return value

        return default

    def dict_dot(self, search, dictionary, default=""):
        """Takes a dot notation representation of a dictionary and fetches it from the dictionary.

        This will take something like s3.locations and look into the s3 dictionary and fetch the locations
        key.

        Arguments:
            search {string} -- The string to search for in the dictionary using dot notation.
            dictionary {dict} -- The dictionary to search through.

        Returns:
            string -- The value of the dictionary element.
        """
        return self.dot(search, dictionary, default)

    def find(self, search_path, default=""):
        """Used for finding both the uppercase and specified version.

        Arguments:
            search_path {string} -- The search path to find the module,
                                    dictionary key, object etc. This is typically
                                    in the form of dot notation 'config.application.debug'

        Keyword Arguments:
            default {string} -- The default value to return if the search path
                                could not be found. (default: {''})

        Returns:
            any -- Could be a string, object or anything else that is fetched.
        """
        value = pydoc.locate(search_path)

        if value:
            return value

        paths = search_path.split(".")

        value = pydoc.locate(".".join(paths[:-1]) + "." + paths[-1].upper())

        if value or value is False:
            return value

        search_path = -1

        # Go backwards through the dot notation until a match is found.
        ran = 0
        while ran < len(paths):
            try:
                value = pydoc.locate(
                    ".".join(paths[:search_path]) + "." + paths[search_path].upper()
                )
            except IndexError:
                return default

            if value:
                break

            value = pydoc.locate(
                ".".join(paths[:search_path]) + "." + paths[search_path]
            )

            if value:
                break

            search_path -= 1
            ran += 1

        if not value or inspect.ismodule(value):
            return default

        return value


def compile_route_to_url(route, params={}):
    """Compile the route url into a usable url.

    Converts /url/@id into /url/1. Used for redirection

    Arguments:
        route {string} -- An uncompiled route
                            like (/dashboard/@user:string/@id:int)

    Keyword Arguments:
        params {dict} -- Dictionary of parameters to pass to the route (default: {{}})

    Returns:
        string -- Returns a compiled string (/dashboard/joseph/1)
    """
    if "http" in route:
        return route

    # Split the url into a list
    split_url = route.split("/")

    # Start beginning of the new compiled url
    compiled_url = "/"

    # Iterate over the list
    for url in split_url:
        if url:
            # if the url contains a parameter variable like @id:int
            if "@" in url:
                url = url.replace("@", "").split(":")[0]
                if isinstance(params, dict):
                    compiled_url += str(params[url]) + "/"
                elif isinstance(params, list):
                    compiled_url += str(params.pop(0)) + "/"
            elif "?" in url:
                url = url.replace("?", "").split(":")[0]
                if isinstance(params, dict):
                    compiled_url += str(params.get(url, "/")) + "/"
                elif isinstance(params, list):
                    compiled_url += str(params.pop(0)) + "/"
            else:
                compiled_url += url + "/"

    compiled_url = compiled_url.replace("//", "")
    # The loop isn't perfect and may have an unwanted trailing slash
    if compiled_url.endswith("/") and not route.endswith("/"):
        compiled_url = compiled_url[:-1]

    # The loop isn't perfect and may have 2 slashes next to eachother
    if "//" in compiled_url:
        compiled_url = compiled_url.replace("//", "/")

    return compiled_url


def cookie_expire_time(str_time):
    """Take a string like 1 month or 5 minutes and returns a pendulum instance.

    Arguments:
        str_time {string} -- Could be values like 1 second or 3 minutes

    Returns:
        pendulum -- Returns Pendulum instance
    """
    import pendulum

    if str_time != "expired":
        number = int(str_time.split(" ")[0])
        length = str_time.split(" ")[1]

        if length in ("second", "seconds"):
            # Sat, 06 Jun 2020 15:36:16 GMT
            return (
                pendulum.now("GMT")
                .add(seconds=number)
                .format("ddd, DD MMM YYYY H:mm:ss")
            )
        elif length in ("minute", "minutes"):
            return (
                pendulum.now("GMT")
                .add(minutes=number)
                .format("ddd, DD MMM YYYY H:mm:ss")
            )
        elif length in ("hour", "hours"):
            return (
                pendulum.now("GMT").add(hours=number).format("ddd, DD MMM YYYY H:mm:ss")
            )
        elif length in ("days", "days"):
            return (
                pendulum.now("GMT").add(days=number).format("ddd, DD MMM YYYY H:mm:ss")
            )
        elif length in ("week", "weeks"):
            return pendulum.now("GMT").add(weeks=1).format("ddd, DD MMM YYYY H:mm:ss")
        elif length in ("month", "months"):
            return (
                pendulum.now("GMT")
                .add(months=number)
                .format("ddd, DD MMM YYYY H:mm:ss")
            )
        elif length in ("year", "years"):
            return (
                pendulum.now("GMT").add(years=number).format("ddd, DD MMM YYYY H:mm:ss")
            )

        return None
    else:
        return pendulum.now("GMT").subtract(years=20).format("ddd, DD MMM YYYY H:mm:ss")


class HasColoredCommands:
    def success(self, message):
        print("\033[92m {0} \033[0m".format(message))

    def warning(self, message):
        print("\033[93m {0} \033[0m".format(message))

    def danger(self, message):
        print("\033[91m {0} \033[0m".format(message))

    def info(self, message):
        return self.success(message)


def password(password_string):
    """Bcrypt a string.

    Useful for storing passwords in a database.

    Arguments:
        pass {string} -- A string like a users plain text password to be bcrypted.

    Returns:
        string -- The encrypted string.
    """
    import bcrypt

    return bytes(
        bcrypt.hashpw(bytes(password_string, "utf-8"), bcrypt.gensalt())
    ).decode("utf-8")


def optional(attribute, default=None, is_method=False):
    """Wrap an object on which any attributes/methods can be called
    without raising an error if it does not exist. It will return a default value of None instead,
    which can be overriden.

    If you want to call method on the wrapped object, is_method should be set to True."""

    class OptionalWrapper(object):
        def __init__(self, obj, default, is_method):
            self._obj = obj
            self._default = default
            self._is_method = is_method

        def __getattr__(self, attr):
            try:
                return getattr(self._obj, attr)
            except AttributeError:
                if self._is_method:
                    return lambda: self._default
                else:
                    return self._default

    return OptionalWrapper(attribute, default, is_method)

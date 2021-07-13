from .structures import load
import random
import string


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


class AssetHelper:
    def __init__(self, app):
        self.app = app

    def asset(self, alias, file_name):
        disks = load(self.app.make("config.filesystem")).DISKS

        if "." in alias:
            alias = alias.split(".")
            location = disks[alias[0]]["path"][alias[1]]
            if location.endswith("/"):
                location = location[:-1]

            return "{}/{}".format(location, file_name)

        location = disks[alias]["path"]
        if isinstance(location, dict):
            location = list(location.values())[0]
            if location.endswith("/"):
                location = location[:-1]

        return "{}/{}".format(location, file_name)


class UrlHelper:
    def __init__(self, app):
        self.app = app

    def url(self, url):
        base_url = self.app.make("base_url").rstrip(
            "/"
        )  # just ensure that no slash is appended to the url

        return f"{base_url}/{url}"


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


class DefaultType:
    def __init__(self, value):
        self.value = value

    def __getattr__(self, attr):
        return self.value

    def __call__(self, *args, **kwargs):
        return self.value

    def __eq__(self, other):
        if self.value is None:
            return other is self.value
        else:
            return other == self.value


class Optional:
    def __init__(self, obj, default=None):
        self.obj = obj
        self.default = default

    def __getattr__(self, attr):
        if hasattr(self.obj, attr):
            return getattr(self.obj, attr)
        return DefaultType(self.default)

    def __call__(self, *args, **kwargs):
        return DefaultType(self.default)

    def instance(self):
        return self.obj


def random_string(length=4):
    """Generate a random string based on the length given.

    Keyword Arguments:
        length {int} -- The amount of the characters to generate (default: {4})

    Returns:
        string
    """
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )

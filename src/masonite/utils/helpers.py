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

from .Input import Input
from urllib.parse import parse_qs
from collections import defaultdict
import urllib
import re
import json
import cgi
import re
from ..utils.structures import Dot
from ..filesystem import UploadedFile


class InputBag:
    def __init__(self):
        self.query_string = {}
        self.post_data = {}
        self.environ = {}

    def load(self, environ):
        self.environ = environ
        self.query_string = {}
        self.post_data = {}
        self.parse(environ)
        return self

    def parse(self, environ):
        if "QUERY_STRING" in environ:
            self.query_string = self.query_parse(environ["QUERY_STRING"])

        if "wsgi.input" in environ:
            if "application/json" in environ.get("CONTENT_TYPE", ""):
                try:
                    request_body_size = int(environ.get("CONTENT_LENGTH", 0))
                except (ValueError):
                    request_body_size = 0

                request_body = environ["wsgi.input"].read(request_body_size)

                if isinstance(request_body, bytes):
                    request_body = request_body.decode("utf-8")

                json_payload = json.loads(request_body or "{}")
                if isinstance(json_payload, list):
                    pass
                else:
                    for name, value in json.loads(request_body or "{}").items():
                        self.post_data.update({name: Input(name, value)})

            elif "application/x-www-form-urlencoded" in environ.get("CONTENT_TYPE", ""):
                try:
                    request_body_size = int(environ.get("CONTENT_LENGTH", 0))
                except (ValueError):
                    request_body_size = 0

                request_body = environ["wsgi.input"].read(request_body_size)
                parsed_request_body = urllib.parse.parse_qs(
                    bytes(request_body).decode("utf-8")
                )

                tmp_post_data = defaultdict(dict)
                for name, value in parsed_request_body.items():
                    if name.endswith("[]"):
                        tmp_post_data.update({name[:-2]: value})
                    elif name.endswith("]"):
                        # either comments[description] or comments[description][nested]
                        groups = re.match(
                            r"(?P<name>[^\[]+)\[(?P<value>[^\]]+)\]", name
                        ).groupdict()
                        name = groups["name"]
                        tmp_post_data[name].update({groups["value"]: value})
                        # if len(groups["value"]) == 1:
                        #     tmp_post_data[name].update({groups["value"][0]: value})
                        # else:
                        #     tmp_post_data[name][groups["value"][0]].update(
                        #         {groups["value"][1]: value}
                        #     )
                    else:
                        tmp_post_data.update({name: value})

                for root_name, value in tmp_post_data.items():
                    self.post_data.update({root_name: Input(name, value)})

            elif "multipart/form-data" in environ.get("CONTENT_TYPE", ""):
                try:
                    request_body_size = int(environ.get("CONTENT_LENGTH", 0))
                except (ValueError):
                    request_body_size = 0

                fields = cgi.FieldStorage(
                    fp=environ["wsgi.input"],
                    environ=environ,
                    keep_blank_values=1,
                )

                for name in fields:
                    value = fields.getvalue(name)
                    if isinstance(value, bytes):
                        self.post_data.update(
                            {
                                name: UploadedFile(
                                    fields[name].filename, fields.getvalue(name)
                                )
                            }
                        )
                    else:
                        self.post_data.update(
                            {name: Input(name, fields.getvalue(name))}
                        )
            else:
                try:
                    request_body_size = int(environ.get("CONTENT_LENGTH", 0))
                except (ValueError):
                    request_body_size = 0

                request_body = environ["wsgi.input"].read(request_body_size)
                if request_body:
                    self.post_data.update(
                        json.loads(bytes(request_body).decode("utf-8"))
                    )

    def get(self, name, default=None, clean=True, quote=True):

        input = Dot().dot(name, self.all(), default=default)
        if isinstance(input, (dict, str)):
            return input
        elif hasattr(input, "value"):
            return input.value
        else:
            return input

        return default

    def has(self, *names):
        return all((name in self.all()) for name in names)

    def all(self):
        all = {}
        qs = self.query_string
        if isinstance(qs, list):
            qs = {str(i): v for i, v in enumerate(qs)}

        all.update(qs)
        all.update(self.post_data)
        return all

    def all_as_values(self, internal_variables=False):
        all = self.all()
        new = {}
        for name, input in all.items():
            if not internal_variables:
                if name.startswith("__"):
                    continue
            new.update({name: self.get(name)})

        return new

    def only(self, *args):
        all = self.all()
        new = {}
        for name, input in all.items():
            if name not in args:
                continue
            new.update({name: self.get(name)})

        return new

    def query_parse(self, query_string):
        d = {}
        for name, value in parse_qs(query_string).items():
            regex_match = re.match(r"(?P<name>[^\[]+)\[(?P<value>[^\]]+)\]", name)
            if regex_match:
                gd = regex_match.groupdict()
                d.setdefault(gd["name"], {})[gd["value"]] = Input(name, value[0])
            else:
                d.update({name: Input(name, value[0])})

        return d

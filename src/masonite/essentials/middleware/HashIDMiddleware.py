from ...middleware import Middleware

from ..helpers.hashid import hashid


class HashIDMiddleware(Middleware):
    def before(self, request, response):
        request.input_bag.query_string = hashid(
            request.input_bag.query_string, decode=True
        )
        request.input_bag.post_data = hashid(request.input_bag.post_data, decode=True)
        return request

    def after(self, request, response):

        return request

from ...middleware import Middleware


class ValidationMiddleware(Middleware):
    def before(self, request, response):
        # request.input_bag.query_string = hashid(
        #     request.input_bag.query_string, decode=True
        # )
        # request.input_bag.post_data = hashid(request.input_bag.post_data, decode=True)
        return request

    def after(self, request, response):
        # if validation errors redirect back with errors and input data
        # if validation errors and JSON return JSON error response code 422 ?
        # if request.app.make("session").driver("cookie").has("errors"):
        #     return response.back()

        return request

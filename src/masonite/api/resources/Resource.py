from ...request import Request


class Resource:

    def single(self, request: Request, user_id):
        return self.to_dict(request, self.show(request, user_id))

    def collection(self, request: Request):
        pagination = User.paginate(request.input("limit", 10), request.input("page", 1))
        result = []
        for model in pagination.result:
            result.append(self.to_dict(request, model))
        pagination.result = model.new_collection(result)
        return pagination

    def to_dict(self, request, model):
        return {}

    def when(self, conditional, callback, default=None):
        if conditional:
            return callback()

        return default

    def relation(self, conditional, default=None):
        if conditional:
            return conditional.serialize()

        return default

from masonite.api.resources import Resource


class __class__(Resource):
    def show(self, request, __record___id):
        return __model__.find(__record___id)

    def index(self, request):
        return __model__.paginate(request.input("limit", 20), request.input("page", 1))

    def to_dict(self, request, model):
        return {
            #
        }

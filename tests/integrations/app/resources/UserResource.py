from src.masonite.api.resources import Resource
from src.masonite.request import Request
from ...app.User import User

class UserResource(Resource):

    def single(self, request: Request, user_id):
        return User.find(user_id)

    def collection(self, request: Request):
        return User.paginate(request.input("limit", 20), request.input("page", 1))

    def to_dict(self, request, model):
        return {
            #
        }

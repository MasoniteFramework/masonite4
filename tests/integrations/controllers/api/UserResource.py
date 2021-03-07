from ...app.User import User
from src.masonite.api.resources import Resource


class UserResource(Resource):
    def show(self, request, user_id):
        return User.find(user_id)

    def index(self, request):
        return User.paginate(request.input("limit", 10), request.input("page", 1))

    def to_dict(self, request, model):
        return {
            "name": model.name,
            "email": model.email,
            "profile": self.relation(model.profile),
        }

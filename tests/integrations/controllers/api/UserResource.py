from ...app.User import User

class UserResource:

    def show(self, user_id):
        return User.find(user_id)

    def index(self):
        return User.all()

    def store(self):
        pass

    def update(self):
        pass

    def delete(self, user_id):
        user = User.find(user_id)
        user.delete(user_id)
        return user

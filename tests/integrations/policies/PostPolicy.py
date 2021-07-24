from src.masonite.authorization import Policy


class PostPolicy(Policy):
    def create(self, user):
        return user.email == "idmann509@gmail.com"

    def view_any(self, user):
        return False

    def view(self, user, instance):
        return False

    def update(self, user, instance):
        return user.id == instance.user_id

    def delete(self, user, instance):
        return False

    def force_delete(self, user, instance):
        return False

    def restore(self, user, instance):
        return False

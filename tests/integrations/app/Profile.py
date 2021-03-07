from masoniteorm.models import Model


class Profile(Model):
    __fillable__ = ["name", "password", "email"]

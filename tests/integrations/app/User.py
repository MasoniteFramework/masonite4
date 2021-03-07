from masoniteorm.models import Model
from masoniteorm.relationships import belongs_to
from src.masonite.authentication import Authenticates


class User(Model, Authenticates):
    __fillable__ = ["name", "password", "email"]

    @belongs_to("id", "user_id")
    def profile(self):
        from .Profile import Profile

        return Profile

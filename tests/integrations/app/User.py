from masoniteorm.models import Model
from src.masonite.authentication import Authenticates


class User(Model, Authenticates):
    pass

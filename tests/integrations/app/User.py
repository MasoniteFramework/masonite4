from masoniteorm.models import Model
from src.masonite.auth import Authenticates

class User(Model, Authenticates):
    pass

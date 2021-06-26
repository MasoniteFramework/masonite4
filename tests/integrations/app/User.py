from masoniteorm.models import Model
from src.masonite.authentication import Authenticates
from src.masonite.notification import Notifiable


class User(Model, Authenticates, Notifiable):
    __fillable__ = ["name", "password", "email", "phone"]

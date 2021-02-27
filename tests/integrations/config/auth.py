import os
from ..app.User import User

GUARDS = {
    "default": "web",
    "web": {
        "model": User
    } 
}

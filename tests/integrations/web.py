from src.masonite.routes import Route
from src.masonite.broadcasting import Broadcast
from src.masonite.authentication import Auth
from tests.integrations.app.User import User
from .app.resources.UserResource import UserResource


Route.group(
    Route.get("/", "WelcomeController@show").name("welcome"),
    Route.post("/", "WelcomeController@show"),
    Route.post("/upload", "WelcomeController@upload").name("upload"),
    Route.get("/test", "WelcomeController@test"),
    Route.get("/emit", "WelcomeController@emit"),
    Route.get("/view", "WelcomeController@view"),
    Route.get("/mail", "MailableController@view"),
    middleware=("web",),
)

Route.group(
    Route.get("/protected", "WelcomeController@protect"),
    Route.get("/users", UserResource.collection).name("users.collection"),
    Route.get("/users/@id", UserResource.single).name("users.single"),
    middleware=("api",),
    prefix="/api",
)

Broadcast.routes()
Auth.routes()

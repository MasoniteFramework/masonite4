from src.masonite.routes import Route
from src.masonite.broadcasting import Broadcast
from src.masonite.authentication import Auth

ROUTES = [
    Route.get("/", "WelcomeController@show").name("welcome"),
    Route.post("/", "WelcomeController@show"),
    Route.post("/upload", "WelcomeController@upload").name("upload"),
    Route.get("/test", "WelcomeController@test"),
    Route.get("/emit", "WelcomeController@emit"),
    Route.get("/view", "WelcomeController@view"),
    Route.get("/mail", "MailableController@view"),
]

Broadcast.routes()
Auth.routes()

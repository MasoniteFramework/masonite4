from src.masonite.routes import Route
from src.masonite.broadcasting import Broadcast
from src.masonite.authentication import Auth

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
    Route.get("/users", "api.UserResource@index").name('users.index'), 
    Route.get("/users/@id", "api.UserResource@show").name('users.show'), 
    middleware=("api",),
    prefix="/api"
)

Broadcast.routes()
Auth.routes()
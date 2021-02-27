from src.masonite.routes import Route
from src.masonite.broadcasting.BroadcastRoutes import BroadcastRoutes

Route.get("/", "WelcomeController@show").name("welcome"),
Route.post("/", "WelcomeController@show"),
Route.post("/upload", "WelcomeController@upload").name("upload"),
Route.get("/test", "WelcomeController@test"),
Route.get("/emit", "WelcomeController@emit"),
Route.get("/view", "WelcomeController@view"),
Route.get("/mail", "MailableController@view"),

Route.get('/login', "auth.LoginController@show").name("login")
Route.get('/register', "auth.RegisterController@show").name("register")
Route.post('/register', "auth.RegisterController@store").name("register.store")
Route.post('/login', "auth.LoginController@store").name("login.store")

BroadcastRoutes.routes()

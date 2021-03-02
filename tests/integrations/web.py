from src.masonite.routes import Route
from src.masonite.broadcasting import Broadcast
from src.masonite.authentication import Auth

Route.get("/", "WelcomeController@show").name("welcome"),
Route.post("/", "WelcomeController@show"),
Route.post("/upload", "WelcomeController@upload").name("upload"),
Route.get("/test", "WelcomeController@test"),
Route.get("/emit", "WelcomeController@emit"),
Route.get("/view", "WelcomeController@view"),
Route.get("/mail", "MailableController@view"),

# Route.get("/login", "auth.LoginController@show").name("login")
# Route.get("/home", "auth.HomeController@show").name("auth.home")
# Route.get("/register", "auth.RegisterController@show").name("register")
# Route.post("/register", "auth.RegisterController@store").name("register.store")
# Route.get("/password_reset", "auth.PasswordResetController@show").name("password_reset")
# Route.post("/password_reset", "auth.PasswordResetController@store").name(
#     "password_reset.store"
# )
# Route.get("/change_password", "auth.PasswordResetController@change_password").name(
#     "change_password"
# )
# Route.post(
#     "/change_password", "auth.PasswordResetController@store_changed_password"
# ).name("change_password.store")
# Route.post("/login", "auth.LoginController@store").name("login.store")
# Route.post("/login", "auth.LoginController@store").name("login.store")

Broadcast.routes()
Auth.routes()

from src.masonite.routes import Route

Route.get("/", "WelcomeController@show").name("welcome"),
Route.post("/", "WelcomeController@show"),
Route.post("/upload", "WelcomeController@upload").name("upload"),
Route.get("/test", "WelcomeController@test"),
Route.get("/view", "WelcomeController@view"),
Route.get("/mail", "MailableController@view"),

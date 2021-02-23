from src.masonite.routes import Route

Route.get("/", "WelcomeController@show"),
Route.post("/", "WelcomeController@show"),
Route.post("/upload", "WelcomeController@upload"),
Route.get("/test", "WelcomeController@test"),
Route.get("/view", "WelcomeController@view"),
Route.get("/mail", "MailableController@view"),

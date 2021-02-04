from src.masonite.routes import Route

Route.get("/", "WelcomeController@show"),
Route.post("/", "WelcomeController@show"),
Route.get("/test", "WelcomeController@test"),
Route.get("/view", "WelcomeController@view"),

from src.masonite.routes import Route

Route.get("/", "WelcomeController@show")

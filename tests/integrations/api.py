from src.masonite.routes import Route

Route.get("/try", "WelcomeController@show").name("welcome"),


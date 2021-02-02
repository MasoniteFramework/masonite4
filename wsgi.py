from src.masonite.foundation import Application, response_handler, Kernel
from src.masonite.providers import FrameworkProvider, RouteProvider, ViewProvider
import os


application = Application(os.getcwd())

"""First Bind important providers needed to start the server
"""

application.register_providers(
    Kernel,
)

"""Bind important keys to the application. TODO: make this all bound maybe in a new Kernel class
"""
application.add_providers(
    FrameworkProvider,
    RouteProvider,
    ViewProvider
)




from src.masonite.foundation import Application, response_handler, Kernel
from src.masonite.providers import FrameworkProvider, RouteProvider, ViewProvider
from tests.integrations.config.providers import PROVIDERS
import os


application = Application(os.getcwd())

"""First Bind important providers needed to start the server
"""

application.register_providers(
    Kernel,
)

application.add_providers(*PROVIDERS)




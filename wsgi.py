from src.masonite.foundation import Application, Kernel, HttpKernel
from tests.integrations.config.providers import PROVIDERS
import os


application = Application(os.getcwd())

"""First Bind important providers needed to start the server
"""

application.register_providers(
    Kernel,
    HttpKernel
)

application.add_providers(*PROVIDERS)

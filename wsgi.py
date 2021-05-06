from src.masonite.foundation import Application, Kernel, HttpKernel
from tests.integrations.config.providers import PROVIDERS
from tests.integrations.app.Kernel import Kernel as ApplicationKernel
import os



application = Application(os.getcwd())

"""First Bind important providers needed to start the server
"""

application.register_providers(
    Kernel,
    ApplicationKernel,
    HttpKernel
)

application.add_providers(*PROVIDERS)

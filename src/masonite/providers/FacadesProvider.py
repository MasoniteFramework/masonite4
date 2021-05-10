import builtins
from ..providers import Provider


class FacadesProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        for facade_name, container_name in self.application.make("facades").items():
            setattr(builtins, facade_name, self.application.make(container_name))

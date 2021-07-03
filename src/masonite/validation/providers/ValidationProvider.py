"""A Validation Service Provider."""

from ...providers import Provider
from .. import Validator, ValidationFactory, MessageBag
from ..commands.RuleEnclosureCommand import RuleEnclosureCommand
from ..commands.RuleCommand import RuleCommand


class ValidationProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        validator = Validator
        self.application.singleton("Validator", validator)
        self.application.make("commands").add(
            RuleEnclosureCommand(self.application),
            RuleCommand(self.application),
        )

        MessageBag.get_errors = self._get_errors
        self.application.make("view").share({"bag": MessageBag.view_helper})

    def boot(self, validator: Validator):
        validator.extend(ValidationFactory().registry)

    def _get_errors(self):
        request = self.application.make("request")
        messages = []
        for error, message in (
            request.session.get_flashed_messages().get("errors", {}).items()
        ):
            messages += message

        return messages

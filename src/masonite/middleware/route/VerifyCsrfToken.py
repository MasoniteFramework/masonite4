from .. import Middleware
from jinja2 import Markup
import binascii
from ...exceptions import InvalidCSRFToken
import os
from hmac import compare_digest


class VerifyCsrfToken(Middleware):

    exempt = []

    def before(self, request, response):
        self.verify_token(request, self.get_token(request))

        token = self.create_token(request)

        request.app.make("view").share(
            {
                "csrf_field": Markup(
                    "<input type='hidden' name='__token' value='{0}' />".format(token)
                ),
                "csrf_token": token,
            }
        )

        return request

    def after(self, request, response):
        request.cookie("csrf_token", request.cookie("SESSID"))
        return request

    def create_token(self, request):
        return request.cookie("SESSID")

    def verify_token(self, request, token):
        if request.is_not_safe() and not self.in_exempt():
            if request.cookie("csrf_token") and (
                compare_digest(
                    request.app.make("sign").unsign(request.cookie("csrf_token")),
                    request.app.make("sign").unsign(token),
                )
                and compare_digest(
                    request.app.make("sign").unsign(token), request.cookie("SESSID")
                )
            ):
                return True
            raise InvalidCSRFToken("Invalid CSRF token.")
        return True

    def in_exempt(self):
        """Determine if the request has a URI that should pass through CSRF verification.

        Returns:
            bool
        """
        return False
        if not self.exempt:
            return False

        for route in self.exempt:
            # if self.request.contains(route):
            return True

        return False

    def get_token(self, request):
        return (
            request.header("X-CSRF-TOKEN")
            or request.header("X-XSRF-TOKEN")
            or request.input("__token")
        )

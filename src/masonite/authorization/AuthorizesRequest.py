class AuthorizesRequest:
    def authorize(self, permission, *args):
        from ..facades import Gate

        return Gate.authorize(permission, *args)

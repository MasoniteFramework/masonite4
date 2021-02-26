from ..routes import Route


class BroadcastRoutes:
    @classmethod
    def routes(self):
        Route.post("/broadcasting/authorize", BroadcastingController.authorize).name(
            "broadcasting.authorize"
        )


class BroadcastingController:
    def authorize(self):
        return {"authorized": True}

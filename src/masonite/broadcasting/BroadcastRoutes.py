from ..routes import Route
from ..request import Request
from ..broadcasting import Broadcast


class BroadcastRoutes:
    @classmethod
    def routes(self):
        Route.post("/broadcasting/authorize", BroadcastingController.authorize).name(
            "broadcasting.authorize"
        )




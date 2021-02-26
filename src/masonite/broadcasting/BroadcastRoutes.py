from ..routes import Route
from ..request import Request
from ..broadcasting import Broadcast


class BroadcastRoutes:
    @classmethod
    def routes(self):
        Route.post("/broadcasting/authorize", BroadcastingController.authorize).name(
            "broadcasting.authorize"
        )


class BroadcastingController:
    def authorize(self, request: Request, broadcast: Broadcast):
        return broadcast.driver("pusher").authorize(
            request.input("channel_name"), request.input("socket_id")
        )

from ..routes import Route
from ..request import Request
import os
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
        # import pusher

        # pusher_client = pusher.Pusher(
        #     app_id=os.getenv("PUSHER_APP_ID"),
        #     key=os.getenv("PUSHER_CLIENT"),
        #     secret=os.getenv("PUSHER_SECRET"),
        #     cluster=os.getenv("PUSHER_CLUSTER"),
        #     ssl=False,
        # )

        # return pusher_client.authenticate(
        #     channel=request.input("channel_name"), socket_id=request.input("socket_id")
        # )

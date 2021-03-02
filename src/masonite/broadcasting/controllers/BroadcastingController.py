from ..Broadcast import Broadcast
from ...request import Request


class BroadcastingController:
    def authorize(self, request: Request, broadcast: Broadcast):
        return broadcast.driver("pusher").authorize(
            request.input("channel_name"), request.input("socket_id")
        )

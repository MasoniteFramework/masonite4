from src.masonite.providers import (
    RouteProvider,
    FrameworkProvider,
    RouteProvider,
    ViewProvider,
    WhitenoiseProvider,
    ExceptionProvider,
    MailProvider,
    NotificationProvider,
    SessionProvider,
    QueueProvider,
)

from src.masonite.scheduling.providers import ScheduleProvider


PROVIDERS = [
    FrameworkProvider,
    RouteProvider,
    ViewProvider,
    WhitenoiseProvider,
    ExceptionProvider,
    MailProvider,
    NotificationProvider,
    SessionProvider,
    QueueProvider,
    ScheduleProvider,
]

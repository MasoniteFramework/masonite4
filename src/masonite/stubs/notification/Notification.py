from masonite.notification import Notification
from masonite.mail import Mailable


class __class__(Notification):
    def to_mail(self, notifiable):
        return (
            Mailable()
            .to(notifiable.email)
            .subject("Masonite 4")
            .from_("sam@masoniteproject.com")
            .text(f"Hello {notifiable.name}")
        )

    def via(self, notifiable):
        return ["mail"]

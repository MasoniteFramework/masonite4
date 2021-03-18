from masonite.notification import Notification
from masonite.mail import Mailable


class Welcome(Notification):
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

from .Mailable import Mailable

class Welcome(Mailable):

    def build(self):
        (self
            .to("joe")
            .subject("Masonite 4")
            .from_("joe@masoniteproject.com")
            .text("Hello from Masonite!")
            .html("<h1>Hello from Masonite!</h1>")
            .view("mailables.welcome", {})
        )

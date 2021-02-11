from src.masonite.mail import Mail


class MockMail(Mail):

    def send(self, driver=None):
        return "mocked"

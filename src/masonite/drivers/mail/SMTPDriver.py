import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from .Recipient import Recipient


class SMTPDriver:
    def __init__(self, application):
        self.application = application
        self.options = {}

    def set_options(self, options):
        self.options = options
        return self

    def get_mime_message(self):
        message = MIMEMultipart("alternative")

        message["Subject"] = self.options.get("subject")

        message["From"] = Recipient(self.options.get("from")).header()
        message["To"] = Recipient(self.options.get("to")).header()
        if self.options.get("reply_to"):
            message["Reply-To"] = Recipient(self.options.get("reply_to")).header()

        if self.options.get("html_content"):
            message.attach(MIMEText(self.options.get("html_content"), "html"))

        if self.options.get("text_content"):
            message.attach(MIMEText(self.options.get("text_content"), "plain"))

        for attachment in self.options.get("attachments", []):
            with open(attachment.path, "rb") as fil:
                part = MIMEApplication(fil.read(), Name=attachment.alias)
            # After the file is closed
            part["Content-Disposition"] = f"attachment; filename={attachment.alias}"
            message.attach(part)

        return message

    def make_connection(self):
        options = self.options
        smtp = smtplib.SMTP("{0}:{1}".format(options["host"], int(options["port"])))

        if options.get("username") and options.get("password"):
            smtp.login(options.get("username"), options.get("password"))

        return smtp

    def send(self):
        smtp = self.make_connection()

        smtp.send_message(self.get_mime_message())

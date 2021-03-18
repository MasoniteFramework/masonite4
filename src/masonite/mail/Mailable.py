from .MessageAttachment import MessageAttachment


class Mailable:
    def __init__(self):
        self._to = ""
        self._cc = None
        self._bcc = None
        self._from = ""
        self._reply_to = ""
        self._subject = ""
        self._priority = None
        self.text_content = ""
        self.html_content = ""
        self.attachments = []

    def to(self, to):
        self._to = to
        return self

    def cc(self, cc):
        self._cc = cc
        return self

    def bcc(self, bcc):
        self._bcc = bcc
        return self

    def set_application(self, application):
        self.application = application
        return self

    def from_(self, _from):
        self._from = _from
        return self

    def attach(self, name, path):
        self.attachments.append(MessageAttachment(name, path))
        return self

    def reply_to(self, reply_to):
        self._reply_to = reply_to
        return self

    def subject(self, subject):
        self._subject = subject
        return self

    def text(self, content):
        self.text_content = content
        return self

    def html(self, content):
        self.html_content = content
        return self

    def view(self, view, data):
        return self.html(
            self.application.make("view").render(view, data).rendered_template
        )

    def priority(self, priority):
        self._priority = priority
        return self

    def high_priority(self):
        self._priority = 1
        return self

    def low_priority(self):
        self._priority = 5
        return self

    def get_response(self):
        self.build()
        if self.get_options().get("html_content"):
            return self.get_options().get("html_content")
        if self.get_options().get("text_content"):
            return self.get_options().get("text_content")

    def get_options(self):
        return {
            "to": self._to,
            "cc": self._cc,
            "bcc": self._bcc,
            "from": self._from,
            "subject": self._subject,
            "text_content": self.text_content,
            "html_content": self.html_content,
            "reply_to": self._reply_to,
            "attachments": self.attachments,
            "priority": self._priority,
        }

    def build(self, *args, **kwargs):
        return self

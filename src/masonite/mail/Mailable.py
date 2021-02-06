class Mailable:
    def __init__(self):
        self._to = ""
        self._from = ""
        self._reply_to = ""
        self._subject = ""
        self.text_content = ""
        self.html_content = ""

    def to(self, to):
        self._to = to
        return self

    def from_(self, _from):
        self._from = _from
        return self

    # def attach(self, name, attachment):
    #     pass

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

    def view(self, content, data):
        self.html_content = content
        return self

    def get_options(self):
        return {
            "to": self._to,
            "from": self._from,
            "subject": self._subject,
            "text_content": self.text_content,
            "html_content": self.html_content,
            "reply_to": self._reply_to,
        }

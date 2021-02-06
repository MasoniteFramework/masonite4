class Recipient:
    def __init__(self, recipient):
        self.recipient = recipient

    def header(self):
        headers = []
        for address in self.recipient.split(","):

            if "<" in address:
                headers.append(address)
                continue

            headers.append(f"<{address.strip()}>")

        return ", ".join(headers)

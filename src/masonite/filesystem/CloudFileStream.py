import os


class CloudFileStream:
    def __init__(self, stream, name):
        self.stream = stream
        self._name = name

    def extension(self):
        return os.path.splitext(self.name())[1]

    def stream(self):
        return self.stream

    def name(self):
        return self._name

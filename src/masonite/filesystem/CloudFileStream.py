import os


class CloudFileStream:
    def __init__(self, stream, name):
        self.stream = stream
        self._name = name

    def extension(self):
        _, file_extension = os.path.splitext(self.name())
        return file_extension

    def stream(self):
        return self.stream

    def name(self):
        return self._name

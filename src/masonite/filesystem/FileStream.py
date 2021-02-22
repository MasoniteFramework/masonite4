import os


class FileStream:
    def __init__(self, stream):
        self.stream = stream

    def path(self):
        return self.stream.name

    def extension(self):
        return os.path.splitext(self.path())[1]

    def name(self):
        return os.path.basename(self.path())

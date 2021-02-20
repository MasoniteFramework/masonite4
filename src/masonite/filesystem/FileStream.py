import os


class FileStream:
    def __init__(self, stream):
        self.stream = stream

    def path(self):
        return self.stream.name

    def extension(self):
        _, file_extension = os.path.splitext(self.path())
        return file_extension

    def name(self):
        return os.path.basename(self.path())

import os
import hashlib


class UploadedFile:
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

    def path(self):
        pass

    def extension(self):
        return os.path.splitext(self.filename)[1]

    def name(self):
        return self.filename

    def path_name(self):
        return f"{self.name()}{self.extension()}"

    def hash_path_name(self):
        return f"{self.hash_name()}{self.extension()}"

    def stream(self):
        return self.content

    def hash_name(self):
        return hashlib.sha1(bytes(self.name(), "utf-8")).hexdigest()

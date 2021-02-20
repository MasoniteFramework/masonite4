"""Cache Config"""
import os

DISKS = {
    "default": "local",
    "local": {
        "driver": "file",
        "path": os.path.join(os.getcwd(), "storage/framework/filesystem")
        #
    },
    "s3": {
        # "driver": "s3",
        # "host": "127.0.0.1",
        # "port": "6379",
        # "password": "",
        # "name": "masonite4",
    },
}

"""Cache Config"""
import os

DISKS = {
    "default": "local",
    "local": {
        "driver": "file",
        "path": {
            "public": os.path.join(os.getcwd(), "storage/framework/filesystem"),
            "private": os.path.join(os.getcwd(), "storage/private"),
        },
    },
    "s3": {
        "driver": "s3",
        "client": os.getenv("AWS_CLIENT"),
        "secret": os.getenv("AWS_SECRET"),
        "bucket": os.getenv("AWS_BUCKET"),
    },
}

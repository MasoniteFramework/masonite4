"""Cache Config"""

STORES = {
    "default": "local",
    "local": {
        "driver": "file",
        "location": "storage/framework/cache"
        #
    },
}

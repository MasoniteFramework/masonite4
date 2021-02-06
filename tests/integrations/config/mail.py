import os

DRIVER = "sqlite"

DRIVERS = {
    "smtp": {
        "host": os.getenv("MAIL_HOST"),
        "port": os.getenv("MAIL_PORT"),
        "username": os.getenv("MAIL_USERNAME"),
        "password": os.getenv("MAIL_PASSWORD"),
    }
}

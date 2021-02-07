import os


DRIVERS = {
    "default": "smtp",
    "smtp": {
        "host": os.getenv("MAIL_HOST"),
        "port": os.getenv("MAIL_PORT"),
        "username": os.getenv("MAIL_USERNAME"),
        "password": os.getenv("MAIL_PASSWORD"),
    },
    "mailgun": {
        "domain": "mg.masonitecasts.com",
        "secret": "key-041b279f01997633ffffaf40e064e0c3",
    },
}

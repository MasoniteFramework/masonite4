import os

KEY = os.getenv("APP_KEY", "-RkDOqXojJIlsF_I8wWiUq_KRZ0PtGWTOZ676u5HtLg=")


HASHING = {
    "default": "bcrypt",
    "bcrypt": {"rounds": 10},
    "argon": {},
}

import os

KEY = os.getenv("APP_KEY", "-RkDOqXojJIlsF_I8wWiUq_KRZ0PtGWTOZ676u5HtLg=")


HASHING = {
    "default": "bcrypt",
    "bcrypt": {"rounds": 10},
    "argon2": {"memory": 1024, "threads": 2, "time": 2},
}

MIX_BASE_URL = os.getenv("MIX_BASE_URL", None)

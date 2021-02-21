"""Notifications Settings."""
import os

DRIVERS = {
    "slack": {"token": os.getenv("SLACK_TOKEN", "")},
    "vonage": {
        "key": os.getenv("VONAGE_KEY", ""),
        "secret": os.getenv("VONAGE_SECRET", ""),
        "sms_from": os.getenv("VONAGE_SMS_FROM", "+33000000000"),
    },
}
import logging
import requests


def get_comment() -> str:
    logging.info("Requesting comment")
    resp = requests.get("https://dirty.per.computer/porn")
    resp.raise_for_status()

    message = resp.json()["message"]
    logging.info("Received message: %s", message)
    return message

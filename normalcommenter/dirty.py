import logging

import requests

MAX_RETRIES = 2


def get_comment() -> str:
    retries = 0

    while retries <= MAX_RETRIES:
        try:
            logging.info("Requesting comment")
            resp = requests.get("https://dirty.per.computer/porn")
            resp.raise_for_status()

            comment = resp.json()["message"]
            logging.info("Received comment: %s", comment)
            return comment
        except requests.HTTPError:
            logging.exception(
                "HTTP error while getting comment. Retrying %i times.",
                MAX_RETRIES - retries,
            )
            retries += 1

import logging

import requests

URL = "https://dirty.per.computer/api/comment"
MAX_RETRIES = 2


def get_comment() -> str:
    retries = 0

    while retries <= MAX_RETRIES:
        try:
            logging.info("Requesting comment")
            resp = requests.get(URL)
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

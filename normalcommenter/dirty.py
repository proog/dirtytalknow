from logging import getLogger

import requests

logger = getLogger(__name__)

URL = "https://dirty-api.per.computer/api/comment"
MAX_RETRIES = 2


def get_comment() -> str:
    retries = 0

    while retries <= MAX_RETRIES:
        try:
            logger.info("Requesting comment")
            resp = requests.get(URL)
            resp.raise_for_status()

            comment = resp.json()["message"]
            logger.info("Received comment: %s", comment)
            return comment
        except requests.HTTPError:
            logger.exception(
                "HTTP error while getting comment. Retrying %i times.",
                MAX_RETRIES - retries,
            )
            retries += 1

    raise Exception(f"Couldn't get comment in {MAX_RETRIES} attempts")

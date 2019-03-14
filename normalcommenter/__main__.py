import logging
import os
import random
import time
from . import dirty, imaging, twitter
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
access_token = os.environ["TWITTER_ACCESS_TOKEN"]
access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
twitter_api = twitter.Twitter(
    consumer_key, consumer_secret, access_token, access_token_secret
)

while True:
    min_wait = 5 * 60 * 60
    max_wait = 16 * 60 * 60
    wait = random.randint(min_wait, max_wait)
    next_dt = datetime.now() + timedelta(seconds=wait)

    logging.info("Waiting %is (until %s)", wait, next_dt.strftime("%c"))
    time.sleep(wait)

    try:
        comment = dirty.get_comment()
        bg_image = random.choice(imaging.get_available_images())

        try:
            image = imaging.make_image_with_text(bg_image, comment)
            twitter_api.tweet_image(image)
        except Exception:
            logging.exception("Making or posting image failed, posting text instead")
            shortened = (comment[:277] + "...") if len(comment) > 280 else comment
            twitter_api.tweet_text(shortened)

    except Exception:
        logging.exception("Execution error")


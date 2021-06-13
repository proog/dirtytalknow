import logging
import os
import random
import time
from datetime import datetime, timedelta

from . import dirty, imaging, twitter

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

min_wait_secs = 5 * 60 * 60  # 5 hours
max_wait_secs = 16 * 60 * 60  # 16 hours

twitter_api = twitter.Twitter(
    os.environ["TWITTER_CONSUMER_KEY"],
    os.environ["TWITTER_CONSUMER_SECRET"],
    os.environ["TWITTER_ACCESS_TOKEN"],
    os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
)

while True:
    wait_secs = random.randint(min_wait_secs, max_wait_secs)
    next_dt = datetime.now() + timedelta(seconds=wait_secs)

    logging.info(f"Waiting {wait_secs}s (until {next_dt.strftime('%c')})")
    time.sleep(wait_secs)

    try:
        comment = dirty.get_comment()
        (bg_image, position) = random.choice(imaging.get_available_images())

        try:
            image = imaging.make_image_with_text(bg_image, comment, position=position)
            twitter_api.tweet_image(image)
        except imaging.TextFittingException:
            logging.exception("Making image failed, posting text instead")
            twitter_api.tweet_text(comment)
        except:
            logging.exception("Posting image failed")

    except Exception:
        logging.exception("Execution error")

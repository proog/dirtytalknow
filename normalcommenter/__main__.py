import logging
import os
import random
import time
from datetime import datetime, timedelta

from . import dirty, imaging, mastodon, twitter

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

min_wait_secs = 5 * 60 * 60  # 5 hours
max_wait_secs = 16 * 60 * 60  # 16 hours

twitter_api = (
    twitter.Twitter(
        os.environ["TWITTER_CONSUMER_KEY"],
        os.environ["TWITTER_CONSUMER_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN"],
        os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    if os.getenv("TWITTER_CONSUMER_KEY")
    else None
)
mastodon_api = (
    mastodon.Mastodon(
        os.environ["MASTODON_BASE_URL"],
        os.environ["MASTODON_CLIENT_ID"],
        os.environ["MASTODON_CLIENT_SECRET"],
        os.environ["MASTODON_ACCESS_TOKEN"],
    )
    if os.getenv("MASTODON_BASE_URL")
    else None
)


while True:
    wait_seconds = random.randint(min_wait_secs, max_wait_secs)
    next_execution = datetime.now() + timedelta(seconds=wait_seconds)

    logging.info("Waiting %is (until %s)", wait_seconds, next_execution.strftime("%c"))
    time.sleep(wait_seconds)

    try:
        comment = dirty.get_comment()
        (bg_image, position) = random.choice(imaging.get_available_images())

        try:
            image = imaging.make_image_with_text(bg_image, comment, position=position)

            if twitter_api:
                try:
                    twitter_api.tweet_image(image, alt_text=comment)
                except:
                    logging.exception("Posting image to Twitter failed")

            if mastodon_api:
                try:
                    mastodon_api.post_image(image, alt_text=comment)
                except:
                    logging.exception("Posting image to Mastodon failed")

        except imaging.TextFittingException:
            logging.exception("Making image failed, posting text instead")

            if twitter_api:
                try:
                    twitter_api.tweet_text(comment)
                except:
                    logging.exception("Posting text to Twitter failed")

            if mastodon_api:
                try:
                    mastodon_api.post_text(comment)
                except:
                    logging.exception("Posting text to Mastodon failed")

    except KeyboardInterrupt:
        exit(1)

    except:
        logging.exception("Execution error")

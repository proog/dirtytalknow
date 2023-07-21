import textwrap
from logging import getLogger

import tweepy

logger = getLogger(__name__)


class Twitter:
    def __init__(
        self, consumer_key, consumer_secret, access_token, access_token_secret
    ):
        auth = tweepy.OAuth1UserHandler(
            consumer_key, consumer_secret, access_token, access_token_secret
        )

        self.api_v1 = tweepy.API(auth)
        self.api_v2 = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

    def tweet_text(self, text: str):
        text = " ".join(text.splitlines())
        tweets = textwrap.wrap(text, width=280)
        reply_to_id = None

        for tweet in tweets:
            logger.info("Tweeting text: %s", tweet)
            response = self.api_v2.create_tweet(
                text=tweet, in_reply_to_tweet_id=reply_to_id
            )
            reply_to_id = response.data["id"]

    def tweet_image(self, file, filename="image.jpg", alt_text=""):
        logger.info("Uploading media with filename %s", filename)

        # Seek to beginning before uploading https://github.com/tweepy/tweepy/issues/1667#issuecomment-927342823
        file.seek(0)

        media = self.api_v1.media_upload(filename, file=file)
        media_id = media.media_id

        if alt_text:
            logger.info('Adding alt text "%s" to media id: %i', alt_text, media_id)
            self.api_v1.create_media_metadata(media_id, alt_text)

        logger.info("Tweeting media id: %i", media_id)
        self.api_v2.create_tweet(media_ids=[media_id])

import logging
import textwrap

import tweepy


class Twitter:
    def __init__(
        self, consumer_key, consumer_secret, access_token, access_token_secret
    ):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet_text(self, text):
        text = " ".join(text.splitlines())
        tweets = textwrap.wrap(text, width=280)
        reply_to_id = None

        for tweet in tweets:
            logging.info("Tweeting text: %s", tweet)

            reply_kwargs = {"in_reply_to_status_id": reply_to_id}
            reply_to_id = self.api.update_status(tweet, **reply_kwargs).id

    def tweet_image(self, file, filename="image.jpg"):
        logging.info("Uploading media with filename %s", filename)

        # Seek to beginning before uploading https://github.com/tweepy/tweepy/issues/1667#issuecomment-927342823
        file.seek(0)

        media = self.api.media_upload(filename, file=file)
        media_id = media.media_id

        logging.info("Tweeting media id: %i", media_id)
        self.api.update_status("", media_ids=[media_id])

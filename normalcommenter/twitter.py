import logging
import tweepy


class Twitter:
    def __init__(
        self, consumer_key, consumer_secret, access_token, access_token_secret
    ):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet_text(self, text):
        logging.info("Tweeting text: %s", text)
        twitter_api.update_status(text)

    def tweet_image(self, file, filename="image.jpg"):
        logging.info("Uploading media with filename %s", filename)
        media = twitter_api.media_upload(filename=filename, file=file)
        media_id = media.media_id

        logging.info("Tweeting media id: %i", media_id)
        twitter_api.update_status(media_ids=[media_id])

import base64
import os
from io import BytesIO

import pytest

from normalcommenter.twitter import Twitter


@pytest.mark.skip()
def test_twitter_tweet_text():
    twitter_api = Twitter(
        os.environ["TWITTER_CONSUMER_KEY"],
        os.environ["TWITTER_CONSUMER_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN"],
        os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )

    # 300 character text (two posts)
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque condimentum felis porttitor imperdiet ultricies. Duis eget ipsum nunc. Aenean vehicula faucibus risus, ac dapibus dui maximus a. Sed quis magna ex. Nam pharetra est facilisis tortor malesuada placerat nec at ex. Duis blandit lobortist."

    twitter_api.tweet_text(text)


@pytest.mark.skip()
def test_twitter_tweet_image():
    twitter_api = Twitter(
        os.environ["TWITTER_CONSUMER_KEY"],
        os.environ["TWITTER_CONSUMER_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN"],
        os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )

    # A 200x200 dark square PNG
    image_bytes = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAZAAAAGQAQMAAAC6caSPAAAAA1BMVEUfHx/wUtr8AAAAKklEQVR4Ae3BgQAAAADDoPtTH2AK1QAAAAAAAAAAAAAAAAAAAAAAAACAOE+wAAH1KUxJAAAAAElFTkSuQmCC"
    )
    image_stream = BytesIO(image_bytes)

    twitter_api.tweet_image(image_stream, alt_text="A dark square")

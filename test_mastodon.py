import base64
import os
from io import BytesIO

import pytest

from normalcommenter.mastodon import Mastodon


@pytest.mark.skip()
def test_mastodon_post_text():
    mastodon_api = Mastodon(
        os.environ["MASTODON_BASE_URL"],
        os.environ["MASTODON_CLIENT_ID"],
        os.environ["MASTODON_CLIENT_SECRET"],
        os.environ["MASTODON_ACCESS_TOKEN"],
    )

    # 520 character text (two posts)
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque condimentum felis porttitor imperdiet ultricies. Duis eget ipsum nunc. Aenean vehicula faucibus risus, ac dapibus dui maximus a. Sed quis magna ex. Nam pharetra est facilisis tortor malesuada placerat nec at ex. Duis blandit lobortis maximus. Cras pretium sollicitudin sem eu tincidunt. Vestibulum ac nunc pharetra, tincidunt dolor in, tincidunt lectus. Proin viverra quis mauris at congue. Nunc mollis nunc sed felis porta, ut aliquam tortor dapibus nam."

    mastodon_api.post_text(text)


@pytest.mark.skip()
def test_mastodon_post_image():
    mastodon_api = Mastodon(
        os.environ["MASTODON_BASE_URL"],
        os.environ["MASTODON_CLIENT_ID"],
        os.environ["MASTODON_CLIENT_SECRET"],
        os.environ["MASTODON_ACCESS_TOKEN"],
    )

    # A 200x200 dark square PNG
    image_bytes = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAZAAAAGQAQMAAAC6caSPAAAAA1BMVEUfHx/wUtr8AAAAKklEQVR4Ae3BgQAAAADDoPtTH2AK1QAAAAAAAAAAAAAAAAAAAAAAAACAOE+wAAH1KUxJAAAAAElFTkSuQmCC"
    )
    image_stream = BytesIO(image_bytes)

    mastodon_api.post_image(image_stream, alt_text="A dark square")

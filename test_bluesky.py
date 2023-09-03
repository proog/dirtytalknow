import base64
import os
from io import BytesIO

import pytest
from dotenv import load_dotenv

from normalcommenter.bluesky import Bluesky

load_dotenv()


@pytest.mark.skip()
def test_bluesky_post_text():
    bluesky_api = Bluesky(
        os.environ["BLUESKY_BASE_URL"],
        os.environ["BLUESKY_LOGIN"],
        os.environ["BLUESKY_PASSWORD"],
    )

    # 620 character text (3 posts)
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse elementum felis et nisi suscipit, sit amet pretium lorem vestibulum. Aliquam eget ultrices tortor. Nullam eu ornare diam, non aliquam arcu. Proin nulla justo, placerat ut diam suscipit, rhoncus tristique leo. Aenean sed eros quis urna mollis pharetra. Phasellus sem ipsum, rutrum sed urna porttitor, faucibus suscipit tortor. Fusce faucibus quis tellus a lobortis. Vivamus vulputate nibh tortor, sit amet ornare arcu mollis ac. Nunc volutpat, libero condimentum laoreet porta, ex quam laoreet enim, ut convallis turpis erat at mi. Praesent non ultric."
    post_uris = bluesky_api.post_text(text)

    assert len(post_uris) == 3

    # Clean up
    for post_uri in reversed(post_uris):
        bluesky_api.delete_post(post_uri)


@pytest.mark.skip()
def test_bluesky_post_image():
    bluesky_api = Bluesky(
        os.environ["BLUESKY_BASE_URL"],
        os.environ["BLUESKY_LOGIN"],
        os.environ["BLUESKY_PASSWORD"],
    )

    # A 200x200 dark square PNG
    image_bytes = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAZAAAAGQAQMAAAC6caSPAAAAA1BMVEUfHx/wUtr8AAAAKklEQVR4Ae3BgQAAAADDoPtTH2AK1QAAAAAAAAAAAAAAAAAAAAAAAACAOE+wAAH1KUxJAAAAAElFTkSuQmCC"
    )
    image_stream = BytesIO(image_bytes)

    post_uri = bluesky_api.post_image(image_stream, alt_text="A dark square")

    # Clean up
    bluesky_api.delete_post(post_uri)

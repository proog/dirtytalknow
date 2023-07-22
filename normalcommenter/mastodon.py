import textwrap
from logging import getLogger

import mastodon

logger = getLogger(__name__)


class Mastodon:
    def __init__(
        self, base_url: str, client_id: str, client_secret: str, access_token: str
    ):
        self.api = mastodon.Mastodon(
            api_base_url=base_url,
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
        )

    def post_text(self, text: str):
        text = " ".join(text.splitlines())
        posts = textwrap.wrap(text, width=500)
        reply_to_id = None

        for post in posts:
            logger.info("Posting text: %s", post)

            reply_to_id = self.api.status_post(post, in_reply_to_id=reply_to_id).id

    def post_image(self, file, filename="image.jpg", alt_text=None):
        logger.info("Uploading media with filename %s, alt text %s", filename, alt_text)

        # Seek to beginning before uploading
        file.seek(0)

        media = self.api.media_post(
            file,
            file_name=filename,
            description=alt_text,
            mime_type="image/jpeg",
            focus=(-1, 1),  # Focus thumbnails on the top-left corner
        )
        media_id = media.id

        logger.info("Posting media id: %i", media_id)
        self.api.status_post("", media_ids=[media_id])

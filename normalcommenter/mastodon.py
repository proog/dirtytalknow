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

    def post_text(self, text: str) -> list[int]:
        text = " ".join(text.splitlines())
        posts = textwrap.wrap(text, width=500)
        post_ids = []

        for post in posts:
            logger.info("Posting text: %s", post)

            reply_to_id = post_ids[-1] if len(post_ids) > 0 else None
            post_id = self.api.status_post(post, in_reply_to_id=reply_to_id).id
            post_ids.append(post_id)

        return post_ids

    def post_image(self, file, filename="image.jpg", alt_text=None) -> int:
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
        post_id = self.api.status_post("", media_ids=[media_id]).id

        return post_id

    def delete_post(self, post_id: int):
        logger.info("Deleting post id: %i", post_id)
        self.api.status_delete(post_id)

    def __str__(self) -> str:
        return "Mastodon"

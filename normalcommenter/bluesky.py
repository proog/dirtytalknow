import textwrap
from logging import getLogger

from atproto import AtUri, Client, models

logger = getLogger(__name__)


class Bluesky:
    def __init__(self, base_url: str, login: str, password: str):
        self.api = Client(base_url)
        self.api.login(login, password)

    def post_text(self, text: str) -> list[str]:
        text = " ".join(text.splitlines())
        posts = textwrap.wrap(text, width=300)
        post_refs: list[models.ComAtprotoRepoStrongRef.Main] = []

        for post in posts:
            logger.info("Posting text: %s", post)

            reply_ref = (
                models.AppBskyFeedPost.ReplyRef(post_refs[-1], post_refs[0])
                if len(post_refs) > 0
                else None
            )

            post_ref = self.api.send_post(text=post, reply_to=reply_ref)
            post_refs.append(post_ref)

        return [ref.uri for ref in post_refs]

    def post_image(self, file, alt_text=None) -> str:
        logger.info('Posting media with alt text "%s"', alt_text)

        # Seek to beginning before uploading
        file.seek(0)

        response = self.api.send_image(text="", image=file, image_alt=alt_text)
        return response.uri

    def delete_post(self, post_uri: str):
        logger.info("Deleting post with uri: %s", post_uri)

        post_rkey = AtUri.from_str(post_uri).rkey
        self.api.delete_post(post_rkey)

    def __str__(self) -> str:
        return "Bluesky"

import os

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

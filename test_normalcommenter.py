import os
import pytest
import random
import time
from normalcommenter import imaging


@pytest.mark.parametrize(
    "name, comment",
    [
        (
            "longest",
            "Lorem ipsum dolor sit amet, hinc audiam tritani te nam, no quo fabulas intellegam, quis bonorum ei est. Ne vide malis probatus mei, vivendo moderatius sea ut. Vix honestatis dissentiunt no, duo ad rebum novum. Vel legimus explicari deseruisse eu. Ius at tollit recusabo scriptorem, te dicit accusata nominati pri. No est sumo utroque tacimates. Tollit putent consectetuer cu usu, et soluta audiam insolens nec.",
        ),
        (
            "longer",
            "Cu homero audiam adversarium usu. Petentium repudiare splendide vim id, an nobis laudem sensibus his. At est saperet alienum posidonium, ex nam dicant instructior? Errem facilisi reprehendunt et pro, no duo novum everti alterum. Vix te tibique euripidis, an dico nihil eos!",
        ),
        (
            "long",
            "Nam eu nibh dicunt! Amet partem temporibus et eum? Fuisset minimum eu pro, oblique propriae eam an, sed assum iracundia an! Nihil iriure quo at, appareat invidunt tincidunt mel te!",
        ),
        ("short", "Tincidunt abhorreant eum et. Sed an brute euismod."),
        ("shorter", "Ut eum inani nominavi?"),
        ("shortest", "Ut eum"),
    ],
)
def test_make_image_with_text(name, comment):
    os.makedirs("test-output", exist_ok=True)

    bg_image = random.choice(imaging.get_available_images())
    image = imaging.make_image_with_text(bg_image, comment)
    imaging.write_image_to_file(image, "test-output/img-%s.jpg" % name)

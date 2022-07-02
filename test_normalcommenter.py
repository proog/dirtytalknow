import multiprocessing
import os
import os.path

import pytest

from normalcommenter import dirty, imaging


def process_image(test_name, comment, image_path, position):
    image = imaging.make_image_with_text(image_path, comment, position=position)
    imaging.write_image_to_file(
        image, "test-output/img-%s-%s.jpg" % (os.path.basename(image_path), test_name)
    )


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
    args = [(name, comment, img, pos) for (img, pos) in imaging.get_available_images()]

    with multiprocessing.Pool() as pool:
        pool.starmap(process_image, args)


def test_TextFittingException():
    comment = "Lorem ipsum dolor sit amet, hinc audiam tritani te nam, no quo fabulas intellegam, quis bonorum ei est. Ne vide malis probatus mei, vivendo moderatius sea ut. Vix honestatis dissentiunt no, duo ad rebum novum. Vel legimus explicari deseruisse eu. Ius at tollit recusabo scriptorem, te dicit accusata nominati pri. No est sumo utroque tacimates. Tollit putent consectetuer cu usu, et soluta audiam insolens nec."
    with pytest.raises(imaging.TextFittingException):
        imaging.fit_text_to_image(imaging.FONT_FILE, comment, 100, 100)


def test_get_comment():
    comment = dirty.get_comment()
    assert len(comment) > 0

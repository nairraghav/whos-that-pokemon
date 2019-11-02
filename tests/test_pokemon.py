from pokemon import app
from pytest import mark
# TODO: need to re-write tests


@mark.skip('Changed formatting of unseen pokemon')
def test_get_random_pokemon_returns_none():
    app.UNSEEN_POKEMON = []
    assert not app.get_random_pokemon()


@mark.skip('Changed formatting of unseen pokemon')
def test_get_random_pokemon():
    app.UNSEEN_POKEMON = [475]
    assert app.get_random_pokemon().name == "Gallade"


def test_get_image_path():
    assert app.get_image_path(5) == "static/img/005.png"

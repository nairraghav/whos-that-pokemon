"""Handles the database helpers used to create, fill, destroy the database"""
import requests
from bs4 import BeautifulSoup
from pokemon.config import DB
from pokemon.models.pokemon_model import Pokemon
import urllib


def init_db():  # pragma: no cover
    """Calls the creation of the database"""
    DB.create_all()


def drop_db():  # pragma: no cover
    """Drops the database"""
    DB.drop_all()


# TODO: Gather images again but abstract the url
#       Put the path in the DB
def seed_db():  # pragma: no cover
    """Seeds the database with the correct mapping of each pokemons index and
    other information"""
    for index in range(890):
        pokemon_url = f"https://www.pokemon.com/us/pokedex/{index+1}"
        request = requests.get(pokemon_url)
        soup = BeautifulSoup(request.content, features="lxml")

        # get pokemon name
        title = soup.find(
            "div", attrs={"class": "pokedex-pokemon-pagination-title"}
        )
        pokemon_name = title.find("div").text.split("#")[0].strip()

        # download pokemon image to img subdirectory
        image_url = soup.find("div", {"class": "profile-images"}).img["src"]
        urllib.request.urlretrieve(
            image_url, f"pokemon/static/img/{image_url.split('/')[-1]}"
        )

        pokemon = Pokemon(index=index + 1, name=pokemon_name)
        DB.session.add(pokemon)
        print(f"{pokemon_name} - COMPLETED")
    DB.session.commit()

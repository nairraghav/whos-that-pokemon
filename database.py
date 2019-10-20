from config import db
from models.pokemon import Pokemon
import requests
from bs4 import BeautifulSoup


def init_db():
    db.create_all()


def drop_db():
    db.drop_all()


def seed_db():
    for index in range(808):
        pokemon_url = f"https://www.pokemon.com/us/pokedex/{index + 1}"
        request = requests.get(pokemon_url)
        soup = BeautifulSoup(request.content, features='lxml')

        title = soup.find('div', attrs={'class': 'pokedex-pokemon-pagination-title'})
        pokemon_name = title.find('div').text.split('#')[0].strip()
        pokemon = Pokemon(index=index+1, name=pokemon_name)
        db.session.add(pokemon)
    db.session.commit()

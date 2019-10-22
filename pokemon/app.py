from flask import render_template, request, session
from pokemon.config import app
from pokemon import database
from pokemon.models.pokemon_model import Pokemon
import random
import os

app.secret_key = os.getenv('SECURE_KEY')


# TODO: determine how to filter generations

UNSEEN_POKEMON = [i + 1 for i in range(808)]


@app.cli.command('init_db')
def init_db():
    database.init_db()


@app.cli.command('seed_db')
def seed_db():
    database.seed_db()


@app.cli.command('drop_db')
def drop_db():
    database.drop_db()


def get_random_pokemon():
    if len(UNSEEN_POKEMON) != 0:
        pokemon_index = random.choice(UNSEEN_POKEMON)
        UNSEEN_POKEMON.remove(pokemon_index)
        pokemon = Pokemon.query.filter(Pokemon.index == pokemon_index).first()
        return pokemon
    return None


def get_image_path(pokemon_index):
    pokemon_id = "{0:0=3d}".format(pokemon_index)
    return f"static/img/{pokemon_id}.png"


@app.route('/', methods=['GET'])
def whos_that_pokemon(**kwargs):
    if not session.get('pokemon_name') and not session.get('pokemon_index'):
        while True:
            pokemon = get_random_pokemon()
            if pokemon:
                session['pokemon_name'] = pokemon.name
                session['pokemon_index'] = pokemon.index
                session['guess_count'] = 3
                break
        return render_template('home.html', pokemon=session['pokemon_name'],
                               image=get_image_path(session['pokemon_index']),
                               guess_count=session['guess_count'],
                               **kwargs)
    else:
        return render_template('home.html', pokemon=session['pokemon_name'],
                               image=get_image_path(session['pokemon_index']),
                               guess_count=session['guess_count'],
                               **kwargs)


@app.route('/', methods=['POST'])
def guess_that_pokemon():
    pokemon_guess = request.form['guess_pokemon']
    if pokemon_guess.title() == session['pokemon_name']:
        session['pokemon_name'] = None
        session['pokemon_index'] = None
        return whos_that_pokemon(right_pokemon=True)
    else:
        session['guess_count'] -= 1
    if session['guess_count'] > 0:
        return render_template('home.html', pokemon=session['pokemon_name'],
                               image=get_image_path(session['pokemon_index']),
                               wrong_pokemon=True,
                               guess_count=session['guess_count'])
    else:
        session['pokemon_name'] = None
        session['pokemon_index'] = None
        return whos_that_pokemon(new_pokemon=True)

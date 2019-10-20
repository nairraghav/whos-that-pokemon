from flask import render_template, request, session
from config import app
import database
from models.pokemon import Pokemon
import random

app.secret_key = b'\xb6x(\xd67\x1f\xa7\x15\x92\xf1VqU\xe9|\xbcqu\xac\xf6\x16\xa8\x8f\xe5'

unseen_pokemon = [i+1 for i in range(808)]


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
    if len(unseen_pokemon) != 0:
        pokemon_index = random.choice(unseen_pokemon)
        unseen_pokemon.remove(pokemon_index)
        pokemon = Pokemon.query.filter(Pokemon.index == pokemon_index).first()
        return pokemon
    return None


def get_image_path(pokemon_index):
    pokemon_id = "{0:0=3d}".format(pokemon_index)
    return f"static/img/{pokemon_id}.png"


@app.route('/', methods=['GET'])
def whos_that_pokemon(**kwargs):
    pokemon = get_random_pokemon()
    if pokemon:
        session['pokemon_name'] = pokemon.name
        session['pokemon_index'] = pokemon.index
        return render_template('home.html', pokemon=session['pokemon_name'],
                               image=get_image_path(session['pokemon_index']),
                               **kwargs)


@app.route('/', methods=['POST'])
def guess_that_pokemon():
    pokemon_guess = request.form['guess_pokemon']
    if pokemon_guess.title() == session['pokemon_name']:
        return whos_that_pokemon(right_pokemon=True)
    return render_template('home.html', pokemon=session['pokemon_name'],
                           image=get_image_path(session['pokemon_index']),
                           wrong_pokemon=True)

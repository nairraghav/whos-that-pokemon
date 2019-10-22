"""This handles the app logic to serve up APIs and display the app"""
import random
import os
from flask import render_template, request, session
from pokemon.config import APP
from pokemon import database
from pokemon.models.pokemon_model import Pokemon


APP.secret_key = os.getenv('SECURE_KEY')


# TODO: determine how to filter generations

UNSEEN_POKEMON = [i + 1 for i in range(808)]


@APP.cli.command('init_db')
def init_db():  # pragma: no cover
    """Initializes the DB"""
    database.init_db()


@APP.cli.command('seed_db')
def seed_db():  # pragma: no cover
    """Seeds the DB"""
    database.seed_db()


@APP.cli.command('drop_db')
def drop_db():  # pragma: no cover
    """Drops the DB"""
    database.drop_db()


def get_random_pokemon():
    """This helper method grabs a random pokemon index from the UNSEEN_POKEMON
    list. We, then, return the Pokemon associated with that index. Returns
    None if no pokemon left"""
    if len(UNSEEN_POKEMON) != 0:
        pokemon_index = random.choice(UNSEEN_POKEMON)
        UNSEEN_POKEMON.remove(pokemon_index)
        pokemon = Pokemon.query.filter(Pokemon.index == pokemon_index).first()
        return pokemon
    return None  # instead we should return a 'finished' page


def get_image_path(pokemon_index):
    """Give a pokemon index, this helper method returns the format of the
    image."""
    pokemon_id = "{0:0=3d}".format(pokemon_index)
    return f"static/img/{pokemon_id}.png"


@APP.route('/', methods=['GET'])
def whos_that_pokemon(**kwargs):  # pragma: no cover
    """This method handles the main logic of the page. We check to see if we
    have any session data created. If so, we return the page with that session
    data. If not, we get a new pokemon and set it's data in the session,
    finally rendering the page"""
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


@APP.route('/', methods=['POST'])
def guess_that_pokemon():  # pragma: no cover
    """This method handles the logic of submitting a guess to the application.
    For each guess, we check to see if the answer is correct. If not, we look
    at how many guesses have been made. If within the limit (3), we show a
    'you are incorrect' message and let them try again. If they have exceeded
    the limit, we move on to the next pokemon. If they guess correct, we
    display a success message and show another pokemon"""
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

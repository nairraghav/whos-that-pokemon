"""This handles the app logic to serve up APIs and display the app"""
import random
import os
from flask import render_template, request, session
from pokemon.config import APP
from pokemon import database
from pokemon.models.pokemon_model import Pokemon

APP.secret_key = os.getenv("SECURE_KEY")


# TODO: Figure out better way to show a generation is complete
#  but others remain


def set_unknown_pokemon():
    """This helper method is used to set the unknown pokemon global variable"""
    return {
        1: [i for i in range(1, 152)],
        2: [i for i in range(152, 252)],
        3: [i for i in range(252, 387)],
        4: [i for i in range(387, 494)],
        5: [i for i in range(494, 650)],
        6: [i for i in range(650, 722)],
        7: [i for i in range(722, 810)],
        8: [i for i in range(810, 891)],
    }


UNSEEN_POKEMON = set_unknown_pokemon()


@APP.cli.command("init_db")
def init_db():  # pragma: no cover
    """Initializes the DB"""
    database.init_db()


@APP.cli.command("seed_db")
def seed_db():  # pragma: no cover
    """Seeds the DB"""
    database.seed_db()


@APP.cli.command("drop_db")
def drop_db():  # pragma: no cover
    """Drops the DB"""
    database.drop_db()


def get_random_pokemon():
    """This helper method grabs a random pokemon index from the UNSEEN_POKEMON
    list. We, then, return the Pokemon associated with that index. Returns
    None if no pokemon left"""
    generation = random.choice(session["generations"])
    if len(UNSEEN_POKEMON[generation]) != 0:
        pokemon_index = random.choice(UNSEEN_POKEMON[generation])
        UNSEEN_POKEMON[generation].remove(pokemon_index)
        pokemon = Pokemon.query.filter(Pokemon.index == pokemon_index).first()
        return pokemon
    else:
        return None


def get_image_path(pokemon_index):
    """Give a pokemon index, this helper method returns the format of the
    image."""
    pokemon_id = "{0:0=3d}".format(pokemon_index)
    return f"static/img/{pokemon_id}.png"


@APP.route("/", methods=["GET"])
def whos_that_pokemon(**kwargs):  # pragma: no cover
    """This method handles the main logic of the page. We check to see if we
    have any session data created. If so, we return the page with that session
    data. If not, we get a new pokemon and set it's data in the session,
    finally rendering the page"""
    if not session.get("generations"):
        session["generations"] = [i for i in range(1, 9)]
    if not session.get("score"):
        session["score"] = 0

    if not session.get("pokemon_name") and not session.get("pokemon_index"):
        while True:
            pokemon = get_random_pokemon()
            if pokemon:
                session["pokemon_name"] = pokemon.name.lower()
                session["pokemon_index"] = pokemon.index
                session["guess_count"] = 3
                break
            else:
                return render_template("finished.html")

        return render_template(
            "home.html",
            pokemon=session["pokemon_name"],
            image=get_image_path(session["pokemon_index"]),
            generations=session["generations"],
            guess_count=session["guess_count"],
            score=session["score"],
            **kwargs,
        )
    else:
        return render_template(
            "home.html",
            pokemon=session["pokemon_name"],
            image=get_image_path(session["pokemon_index"]),
            generations=session["generations"],
            guess_count=session["guess_count"],
            score=session["score"],
            **kwargs,
        )


@APP.route("/", methods=["POST"])
def guess_that_pokemon():  # pragma: no cover
    """This method handles the logic of submitting a guess to the application.
    For each guess, we check to see if the answer is correct. If not, we look
    at how many guesses have been made. If within the limit (3), we show a
    'you are incorrect' message and let them try again. If they have exceeded
    the limit, we move on to the next pokemon. If they guess correct, we
    display a success message and show another pokemon"""
    # get the guess
    pokemon_guess = request.form["guess_pokemon"]

    # check to see if the guess is correct
    if pokemon_guess.lower().strip() == session["pokemon_name"]:
        # if correct, bump up score and find a new pokemon
        session["score"] += 1
        return get_new_pokemon(right_pokemon=True)
    else:
        # if wrong, reduce count
        session["guess_count"] -= 1

    # check to see how many times we've guessed
    if session["guess_count"] > 0:
        # if we are still able to guess, give wrong message and let them try
        # again
        return render_template(
            "home.html",
            pokemon=session["pokemon_name"],
            image=get_image_path(session["pokemon_index"]),
            generations=session["generations"],
            wrong_pokemon=True,
            guess_count=session["guess_count"],
            score=session["score"],
        )
    else:
        # if out of guesses, get new pokemon
        session["score"] = 0
        return get_new_pokemon(new_pokemon=True)


@APP.route("/gen", methods=["POST"])
def set_pokemon_generation():  # pragma: no cover
    """This method handles the logic for setting the generation to pull
    indices from when the user sets them via the checkboxes"""
    session["generations"] = [
        int(generation) for generation in request.form.getlist("generation")
    ]

    # find a new pokemon
    return get_new_pokemon()


@APP.route("/reset", methods=["POST"])
def reset_game():  # pragma: no cover
    """This method is used to reset the game after the user has finished
    guessing all pokemon"""
    global UNSEEN_POKEMON
    UNSEEN_POKEMON = set_unknown_pokemon()
    session["pokemon_name"] = None
    session["pokemon_index"] = None
    session["guess_count"] = None
    session["score"] = 0
    session["generations"] = [i for i in range(1, 8)]
    return whos_that_pokemon()


def get_new_pokemon(**kwargs):
    """This helper method is used to reset session data so that we pick a new
    pokemon from our list"""
    if session.get("pokemon_index"):
        remove_pokemon_from_unseen_list(session["pokemon_index"])
    session["pokemon_name"] = None
    session["pokemon_index"] = None
    return whos_that_pokemon(**kwargs)


def remove_pokemon_from_unseen_list(pokemon_index):
    for _, pokemon_list in UNSEEN_POKEMON.items():
        if pokemon_index in pokemon_list:
            pokemon_list.remove(pokemon_index)
            return

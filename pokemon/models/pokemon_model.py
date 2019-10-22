"""Handles the Pokemon class used to store/get items from the database"""
from sqlalchemy import Column, Integer, String
from pokemon.config import DB, MARSH


class Pokemon(DB.Model):
    """This class is used to store Pokemon data. We currently only care about
    the index and name"""
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    name = Column(String)


class PokemonSchema(MARSH.Schema):
    """Setting the fields for the Pokemon Schema"""
    class Meta:
        """Settings the fields for the Pokemon Schema"""
        fields = ('id', 'index', 'name')


POKEMON_SCHEMA = PokemonSchema()

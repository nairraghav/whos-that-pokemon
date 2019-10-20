from sqlalchemy import Column, Integer, String
from config import db, marsh


class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    name = Column(String)


class PokemonSchema(marsh.Schema):
    class Meta:
        fields = ('id', 'index', 'name')


pokemon_schema = PokemonSchema()
pokemons_schema = PokemonSchema(many=True)

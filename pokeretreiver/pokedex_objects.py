"""
This module houses the abstract PokedexObject class, and all
of its subclasses. It also contains the factory classes for
creating these objects.
"""

from abc import ABC, abstractmethod


class PokedexObject(ABC):
    @abstractmethod
    def __init__(self, name: str, id: str, **kwargs):
        self.name = name
        self.id = id


class Pokemon(PokedexObject):
    def __init__(self, height: int, weight: int,
                 stats: list, types: (list, str),
                 abilities: list, moves: list, **kwargs):
        super().__init__(**kwargs)
        self.height = height
        self.weight = weight
        self.stats = stats
        self.types = types
        self.abilities = abilities
        self.moves = moves

    def __str__(self):
        return f'\nPokemon: {self.name.capitalize()} ' \
               f'\nId: {self.id}' \
               f'\nHeight: {self.height} decimetres' \
               f'\nWeight: {self.weight} hectograms'
        # f'\nStats: {self.stats}' \
        # f'\nTypes: {self.types}' \
        # f'\nAbilities: {self.abilities}' \


class Ability(PokedexObject):

    def __init__(self, generation: str, effect_entries: list,
                 pokemon: list, **kwargs):
        super().__init__(**kwargs)
        self.generation = generation
        self.effect = effect_entries[0]["effect"]
        self.short_effect = effect_entries[0]["short_effect"]
        self.pokemon = pokemon

    def __str__(self):
        return f'\nName: {self.name.capitalize()} ' \
               f'\nId: {self.id}' \
               f'\nGeneration: {self.generation}' \
               f'\nEffect: {self.effect}'
        # f'\nEffect: {self.short_effect}' \
        # f'\nPokemon: {self.pokemon}'

        # f'\nStats: {self.stats}' \
        # f'\nTypes: {self.types}' \
        # f'\nAbilities: {self.abilities}' \


class Move(PokedexObject):
    def __init__(self, generation: str, accuracy: int,
                 pp: int, power: int, type: str, damage_class: str, effect_entries: list, **kwargs):
        super().__init__(**kwargs)
        self.generation = generation
        self.accuracy = accuracy
        self.pp = pp
        self.power = power
        self.type = type
        self.damage_class = damage_class
        self.short_effect = effect_entries[0]["short_effect"]

    def __str__(self):
        return f'\nName: {self.name.capitalize()} ' \
               f'\nId: {self.id}' \
               f'\nGeneration: {self.generation}' \
               f'\nAccuracy: {self.accuracy}' \
               f'\nPP: {self.pp}' \
               f'\nPower: {self.power}' \
               f'\nType: {self.type}' \
               f'\nDamage Class: {self.damage_class}' \
               f'\nEffect: {self.short_effect}'


class Stat(PokedexObject):
    def __init__(self, is_battle_only: bool, **kwargs):
        super().__init__(**kwargs)
        self.is_battle_only = is_battle_only


class PokedexObjectFactory(ABC):
    @abstractmethod
    def create_object(self, **kwargs) -> PokedexObject:
        pass


class PokemonFactory(PokedexObjectFactory):
    def create_object(self, **kwargs) -> Pokemon:
        return Pokemon(**kwargs)


class AbilityFactory(PokedexObjectFactory):
    def create_object(self, **kwargs) -> Ability:
        return Ability(**kwargs)


class MoveFactory(PokedexObjectFactory):
    def create_object(self, **kwargs) -> Move:
        return Move(**kwargs)


class StatFactory(PokedexObjectFactory):
    def create_object(self, **kwargs) -> Stat:
        return Stat(**kwargs)

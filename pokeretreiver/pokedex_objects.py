"""
This module houses the abstract PokedexObject class, and all
of its subclasses. It also contains the factory classes for
creating these objects.
"""

from abc import ABC, abstractmethod


class PokedexObject(ABC):
    @abstractmethod
    def __init__(self, name, id, **kwargs):
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


class Ability(PokedexObject):
    def __init__(self, generation: str, effect_entries: list,
                 pokemon: list, **kwargs):
        super().__init__(**kwargs)
        self.generation = generation
        self.effect = effect_entries[1]["effect"]
        self.short_effect = effect_entries[1]["short_effect"]
        self.pokemon = pokemon


class Move(PokedexObject):
    def __init__(self, generation: str, accuracy: int,
                 pp: int, power: int, type: str, **kwargs):
        super().__init__(**kwargs)
        self.generation = generation
        self.accuracy = accuracy
        self.pp = pp
        self.power = power
        self.type = type


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

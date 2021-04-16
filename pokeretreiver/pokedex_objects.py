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
                 abilities: list, moves: list,
                 is_expanded=False, **kwargs):
        super().__init__(**kwargs)
        self.height = height
        self.weight = weight
        self.stats = stats
        self.types = types
        self.abilities = abilities
        self.moves = moves
        self.is_expanded = is_expanded

    def __str__(self):
        if self.is_expanded:
            stat_list = map(str, self.stats)
            move_list = map(str, self.moves)
            ability_list = map(str, self.abilities)
            type_list = [types["type"]["name"].title() for types in self.types]

        else:
            stat_list = [stat["stat"]["name"].title() + " = " +
                         str(stat["base_stat"]) + "\n" for stat in self.stats]
            ability_list = [ability["ability"]["name"].title() + "\n" for ability in self.abilities]
            move_list = [move["move"]["name"].title() + ", Level acquired: " +
                         str(move["version_group_details"][0]["level_learned_at"]) + "\n" for move in self.moves]
            type_list = [types["type"]["name"].title() for types in self.types]

        return f'\nPokemon: {self.name.capitalize()} ' \
               f'\nId: {self.id}' \
               f'\nHeight: {self.height} decimetres' \
               f'\nWeight: {self.weight} hectograms' \
               f"\nTypes: {', '.join(type_list)}" \
               f"\nStats:\n------\n{''.join(stat_list)}" \
               f"\nAbilities:\n------\n{''.join(ability_list)}" \
               f"\nMoves:\n------\n{'Move name: '.join(move_list)}" \
               + "\n---------"


class Ability(PokedexObject):

    def __init__(self, generation: list, effect_entries: list,
                 pokemon: list, **kwargs):
        super().__init__(**kwargs)
        self.generation = generation["name"]
        self.effect = effect_entries[1]["effect"]
        self.short_effect = effect_entries[1]["short_effect"]
        self.pokemon = pokemon

    def __str__(self, pokemon_list=None, generation_list=None):
        pokemon_list = [pokemon["pokemon"]["name"].title() for pokemon in self.pokemon]

        return f'\nAbility Name: {self.name.capitalize()} ' \
               f'\nId: {self.id}' \
               f"\nGeneration: {self.generation.capitalize()}" \
               f'\nEffect: {self.effect}' \
               f'\nEffect (Short): {self.short_effect}' \
               f"\nPokemon: {', '.join(pokemon_list)}"


class Move(PokedexObject):
    def __init__(self, generation: str, accuracy: int,
                 pp: int, power: int, type: str, damage_class: str, effect_entries: list, **kwargs):
        super().__init__(**kwargs)
        self.generation = generation['name']
        self.accuracy = accuracy
        self.pp = pp
        self.power = power
        self.type = type['name']
        self.damage_class = damage_class['name']
        self.short_effect = effect_entries[0]["short_effect"]

    def __str__(self):
        return f'\n\nMove Name: {self.name.capitalize()}' \
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

    def __str__(self):
        return f'\nStat Name: {self.name.capitalize()}' \
               f'\nId: {self.id}' \
               f'\nIs Battle Only: {self.is_battle_only}'


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

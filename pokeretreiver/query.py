"""
This module houses the functions that get json data from an endpoint.
"""
from aiohttp import ClientSession
import asyncio
from pokedex import Request
from pokeretreiver.pokedex_objects import PokemonFactory, AbilityFactory, MoveFactory, StatFactory
from enum import Enum


class PokedexMode(Enum):
    POKEMON = "pokemon"
    ABILITY = "ability"
    MOVE = "move"


class QueryMaster:
    @staticmethod
    def execute_request(request: Request) -> list:
        pokedex_object_factory_mapper = {
            PokedexMode.POKEMON: PokemonFactory,
            PokedexMode.ABILITY: AbilityFactory,
            PokedexMode.MOVE: MoveFactory
        }

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(JsonHelper.process_request(request))
        factory = pokedex_object_factory_mapper[request.mode]()
        error = "An error occurred. Skipping this request.\n"

        if request.mode == PokedexMode.POKEMON and request.expanded:
            result = [factory.create_object(**info, is_expanded=True) if len(info) > 0 else error for info in result]
            result = [JsonHelper.expand_attributes(pokemon) if type(pokemon) != str else pokemon for pokemon in result]
        else:
            result = [factory.create_object(**info) if len(info) > 0 else error for info in result]

        return result


class JsonHelper:
    @staticmethod
    async def get_pokedex_object_data(url: str, session: ClientSession) -> dict:
        """
        An async coroutine that executes GET http request. The response is
        converted to a json. The HTTP request and the json conversion are
        asynchronous processes that need to be awaited.
        :param url: a string, endpoint url
        :param session: an HTTP session
        :return: a dict, json representation of response.
        """
        response = await session.request(method="GET", url=url.lower())

        if "200" in str(response.status):
            return await response.json()
        elif "404" in str(response.status):
            return {}

    @staticmethod
    async def process_request(request: Request) -> list:
        """
        This function returns a list of json responses for a single request.
        :param request: a Request object
        :return: list of dict, collection of response data from the endpoint.
        """
        url = f"https://pokeapi.co/api/v2/{request.mode.value}/"
        async with ClientSession() as session:
            list_tasks = [asyncio.create_task(JsonHelper.get_pokedex_object_data(url + id_, session))
                          for id_ in request.input_data]
            responses = await asyncio.gather(*list_tasks)
            return list(responses)

    @staticmethod
    async def get_moves(pokemon):
        async with ClientSession() as session:
            list_moves_tasks = [asyncio.create_task(
                JsonHelper.get_pokedex_object_data(
                    move["move"]["url"], session
                )) for move in pokemon.moves
            ]
            responses = await asyncio.gather(*list_moves_tasks)
            return list(responses)

    @staticmethod
    async def get_abilities(pokemon):
        async with ClientSession() as session:
            list_abilities_tasks = [asyncio.create_task(
                JsonHelper.get_pokedex_object_data(
                    ability["ability"]["url"], session
                )) for ability in pokemon.abilities
            ]
            responses = await asyncio.gather(*list_abilities_tasks)
            return list(responses)

    @staticmethod
    async def get_stats(pokemon):
        async with ClientSession() as session:
            list_stats_tasks = [asyncio.create_task(
                JsonHelper.get_pokedex_object_data(stat["stat"]["url"], session)) for stat in pokemon.stats
            ]
            responses = await asyncio.gather(*list_stats_tasks)
            return list(responses)

    @staticmethod
    def expand_attributes(pokemon):
        loop = asyncio.get_event_loop()

        stats = loop.run_until_complete(JsonHelper.get_stats(pokemon))
        stat_factory = StatFactory()
        pokemon.stats = [stat_factory.create_object(**stat) for stat in stats]

        moves = loop.run_until_complete(JsonHelper.get_moves(pokemon))
        move_factory = MoveFactory()
        pokemon.moves = [move_factory.create_object(**move) for move in moves]

        abilities = loop.run_until_complete(JsonHelper.get_abilities(pokemon))
        ability_factory = AbilityFactory()
        pokemon.abilities = [ability_factory.create_object(**ability) for ability in abilities]

        return pokemon

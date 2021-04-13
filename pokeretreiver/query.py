"""
This module houses the functions that get json data from an endpoint.
"""
from aiohttp import ClientSession, ContentTypeError
import asyncio
from pokedex import Request


class InvalidEntry(Exception):
    def __init__(self, entry: str):
        super().__init__()
        self.entry = entry

    def __str__(self):
        return f"Invalid Entry: " + "{self.entry}"


async def get_pokedex_object_data(id_: str, url: str, session: ClientSession) -> dict:
    """
    An async coroutine that executes GET http request. The response is
    converted to a json. The HTTP request and the json conversion are
    asynchronous processes that need to be awaited.
    :param id_: a string
    :param url: a string, the url minus the id endpoint
    :param session: an HTTP session
    :return: a dict, json representation of response.
    """
    target_url = url + id_
    response = await session.request(method="GET", url=target_url.lower())

    if "200" in str(response.status):
        json_dict = await response.json()
        return json_dict
    elif "404" in str(response.status):
        json_dict = {}

    return json_dict


async def process_request(request: Request) -> list:
    """
    This function returns a list of json responses for a single request.
    :param request: a Request object
    :return: list of dict, collection of response data from the endpoint.
    """
    url = f"https://pokeapi.co/api/v2/{request.mode.value}/"
    async with ClientSession() as session:
        list_tasks = [asyncio.create_task(get_pokedex_object_data(id_, url, session))
                      for id_ in request.input_data]
        responses = await asyncio.gather(*list_tasks)
        return list(responses)

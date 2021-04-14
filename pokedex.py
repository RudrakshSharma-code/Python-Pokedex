"""
This module houses all argparse related classes and functions.
It also holds classes implementing the chain of responsibility
pattern for handling requests from the console.
"""

import argparse
from abc import ABC, abstractmethod
import os.path
import pokeretreiver.query
# from pokeretreiver.query import QueryMaster, PokedexMode


class Request:
    """
    The request object represents a request to the pokedex for certain data.
    The request object comes with certain accompanying configuration options
    as well as a field that holds the result. The attributes are:

        - mode: 'pokemon', 'ability', or 'move' for a related pokedex object
        - input_data: This is the string data to query the pokedex with. Should
        be converted to a list of separate strings representing ids to query
        - input_file: The text file that contains the string ids to query the
        pokedex with. This is None if the input data is directly entered instead
        - expanded - a boolean representing whether the output should show extra
        information or not. This is False by default
        - output: This is the output text file to which we print the results
        of the request
        - result: Placeholder value to hold the result of the request. This does
        not come in with the request, but rather is replaced pokedex objects at
        some point in the handling of the request.

    """
    def __init__(self):
        self.mode = None
        self.input_data = None
        self.input_file = None
        self.expanded = None
        self.output = None
        self.result = None

    def __str__(self):
        return f"Request: Mode: {self.mode}, Input Data: {self.input_data}" \
               f", Input file: {self.input_file}, Output: {self.output}, " \
               f"Expanded: {self.expanded}"


def setup_request_commandline() -> Request:
    """
    Implements the argparse module to accept arguments via the command
    line. This function specifies what these arguments are and parses it
    into an object of type Request. If something goes wrong with
    provided arguments then the function prints an error message and
    exits the application.
    :return: The object of type Request with all the arguments provided
    in it.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",
                        help="The mode the application will be opened in",
                        choices=["pokemon", "ability", "move"])

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--inputdata",
                       help="Either a name (string) or an id (int)")
    group.add_argument("-f", "--inputfile",
                       help="Input file name must end with a .txt extension")

    parser.add_argument("-e", "--expanded",
                        help="Use flag if you want extra information from your query",
                        action="store_true")

    parser.add_argument("-o", "--output",
                        help="Output file name must end with a .txt extension",
                        default="print")

    try:
        args = parser.parse_args()
        request = Request()
        request.mode = pokeretreiver.query.PokedexMode(args.mode)
        request.input_data = args.inputdata
        request.input_file = args.inputfile
        request.output = args.output
        request.expanded = args.expanded
        print(request)
        return request
    except Exception as e:
        print(f"Error! Could not read arguments.\n{e}")
        quit()


class PokedexRequestController:

    def __init__(self):
        file_paths_handler = ValidateFilePathsHandler()
        input_handler = InputHandler()
        query_handler = QueryHandler()
        output_handler = OutputHandler()
        query_handler.set_handler(output_handler)
        input_handler.set_handler(query_handler)
        file_paths_handler.set_handler(input_handler)
        self.start_handler = file_paths_handler

    def execute_request(self, req: Request):
        result = self.start_handler.handle_request(req)
        if not result[1]:
            print("Handler error:", result[0])


class BaseRequestHandler(ABC):
    """
    Baseclass for all handlers that pokedex requests. Each handler
    can maintain a reference to another handler thereby enabling
    the chain of responsibility pattern.
    """

    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def handle_request(self, req: Request) -> (str, bool):
        """
        Each handler would have a specific implementation of how it
        processes a request.
        :param req: a Request
        :return: a tuple where the first element is a string stating the
        outcome and the reason, and the second a bool indicating
        successful handling of the request or not.
        """
        pass

    def set_handler(self, handler):
        """
        Each handler can invoke another handler at the end of it's
        processing a request. This handler needs to implement the
        BaseRequestHandler interface.
        :param handler: a BaseRequestHandler
        """
        self.next_handler = handler


class ValidateFilePathsHandler(BaseRequestHandler):
    """ Validates input and output file paths if given. """

    def handle_request(self, req: Request) -> (str, bool):
        # Checking if the input file exists and is a text file
        if req.input_file is not None:
            if not os.path.isfile(req.input_file):
                return "File does not exist at input path", False
            if not req.input_file.endswith(".txt"):
                return "Input file must be a text file", False
        # Checking if the output file is a text file
        if req.output != "print" and not req.output.endswith(".txt"):
            return "Output file must be a text file", False

        # Return the result of the next handler if there is one
        if self.next_handler is not None:
            return self.next_handler.handle_request(req)
        else:
            return "", True


class InputHandler(BaseRequestHandler):
    """
    Reads in and stores data from input file if there is one.
    Formats the request's input data to a list of string ids.
    """

    def handle_request(self, req: Request) -> (str, bool):
        # If there is an input file, set input_data
        # in the request to the data from the file.
        if req.input_file is None:
            req.input_data = req.input_data.split(" ")
        else:
            with open(req.input_file, mode="r") as input_file:
                req.input_data = input_file.readlines()
        req.input_data = [id_.strip() for id_ in req.input_data]

        # Return the result of the next handler if there is one
        if self.next_handler is not None:
            return self.next_handler.handle_request(req)
        else:
            return "", True


class QueryHandler(BaseRequestHandler):
    """
    Gets all the json responses for the request, and replaces the request's
    result with a list of pokedex objects correlating to the json responses.
    """

    def handle_request(self, req: Request) -> (str, bool):

        req.result = pokeretreiver.query.QueryMaster.execute_request(req)

        # Return the result of the next handler if there is one
        if self.next_handler is not None:
            return self.next_handler.handle_request(req)
        else:
            return "", True


class OutputHandler(BaseRequestHandler):
    """
    Currently prints out the name of each pokedex object
    for each result to console or to the output file.
    """

    def handle_request(self, req: Request) -> (str, bool):
        output = "\n"
        for result in req.result:
            output += result.__str__() + "\n"
        print(output)
        if req.output != "print":
            with open(req.output, mode="w", encoding='utf-8') as output_file:
                output_file.write(output)

        # Return the result of the next handler if there is one
        if self.next_handler is not None:
            return self.next_handler.handle_request(req)
        else:
            return "", True


def main():
    request = setup_request_commandline()
    pokedex = PokedexRequestController()
    pokedex.execute_request(request)


if __name__ == '__main__':
    main()

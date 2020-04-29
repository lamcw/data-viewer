"""Parsers that deserialize."""
import json
import yaml
from abc import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    def parse(self, s):
        pass


class JsonParser(BaseParser):
    def parse(self, s):
        return json.loads(s)


class YamlParser(BaseParser):
    def parse(self, s):
        return yaml.safe_load(s)


class ParserFactory:
    def __init__(self):
        self._parsers = {}

    def register(self, format, parser):
        self._parsers[format] = parser

    def get_parser(self, format):
        try:
            parser = self._parsers[format]
        except KeyError:
            raise ValueError(f"{format} is not a valid format.")
        return parser

    @property
    def parsers(self):
        return self._parsers

    @property
    def supported_types(self):
        return list(self.parsers.keys())


factory = ParserFactory()
factory.register("json", JsonParser)
factory.register("yaml", YamlParser)

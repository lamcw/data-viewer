"""Parsers that deserializes any storage format into native python types."""
import json
import yaml
from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Abstract base class for parsing an arbitrary storage format."""

    @abstractmethod
    def parse(self, s):
        """
        Parse from string.

        :param s: data in certain file format
        :return: python representation of ``s``
        """
        pass


class JsonParser(BaseParser):
    """Convert JSON string to Python data types."""

    def parse(self, s):
        """
        Parse from JSON string. IO objects not supported.

        :param s: JSON string
        :return: python representation of JSON string ``s``
        """
        return json.loads(s)


class YamlParser(BaseParser):
    """Convert YAML string to Python data types."""

    def parse(self, s, loader=yaml.SafeLoader):
        """
        Parse from YAML string.

        :param s: YAML string
        :param loader: yaml loader, defaults to :class:`yaml.Safeloader`
        :return: python representation of YAML string ``s``
        """
        return yaml.load(s, Loader=loader)


class ParserFactory:
    """
    Factory for retrieving parser based on file type/format.

    For example,
    >>> factory = ParserFactory()
    >>> factory.register("xml", XmlParser)
    >>> Parser = factory.get_parser("xml")
    >>> parser = Parser()
    >>> parser.parse(xml_data)
    """

    def __init__(self):  # noqa: D107
        self._parsers = {}

    def register(self, format, parser):
        """
        Register a parser class with an associated file format.

        :param format: file format
        :param parser: parser class to parse ``format``
        """
        self._parsers[format] = parser

    def get_parser(self, format):
        """
        Retrieve a parser given file format.

        :param format: file format
        :return: parser class associated with ``format``
        :raises ValueError: if format is not registered prior to this method call
        """
        try:
            parser = self._parsers[format]
        except KeyError:
            raise ValueError(f"{format} is not a registered format.")
        return parser

    @property
    def parsers(self):
        """
        Get a map of parsers.

        :return: map between file formats and parsers
        :rtype: dict
        """
        return self._parsers

    @property
    def supported_types(self):
        """
        Get a list of supported file formats.

        :return: List of supported file formats
        :rtype: list
        """
        return list(self.parsers.keys())


factory = ParserFactory()
factory.register("json", JsonParser)
factory.register("yaml", YamlParser)

"""Renderer provides an interface to serialize python data types into file formats."""
import json
import yaml
from abc import ABC, abstractmethod


class BaseRenderer(ABC):
    """Abstrace base class for serializing python data types into a file format."""

    @abstractmethod
    def render(self, data):
        """
        Serialize native Python data types into a certain file format.

        :param data: arbitrary data in Python data types
        :return: string encoded according to file format specification
        :rtype: str
        """
        pass


class JsonRenderer(BaseRenderer):
    """Serialize native Python data types into JSON string."""

    def render(self, data):
        """
        Serialize ``data`` into JSON string.

        :param data: Python data types
        :return: JSON string
        :rtype: str
        """
        return json.dumps(data)


class YamlRenderer(BaseRenderer):
    """Serialize native Python data types into YAML string."""

    def render(self, data):
        """
        Serialize ``data`` into YAML string.

        :param data: Python data types
        :return: YAML string
        :rtype: str
        """
        return yaml.dump(data)


class RendererFactory:
    """
    Factory for retrieving renderer based on file type/format.

    For example,
    >>> factory = RendererFactory()
    >>> factory.register("xml", XmlRenderer)
    >>> Renderer = factory.get_renderer("xml")
    >>> renderer = Renderer()
    >>> xml_data = renderer.render([{"a": 1, "b": 2}, {"c": 3}])
    """

    def __init__(self):  # noqa: D107
        self._renderers = {}

    def register(self, format, renderer):
        """
        Register a renderer class with an associated file format.

        :param format: file format
        :param renderer: renderer class
        """
        self._renderers[format] = renderer

    def get_renderer(self, format):
        """
        Retrieve a renderer given file format.

        :param format: file format
        :return: renderer class associated with ``format``
        :raises ValueError: if format is not registered prior to this method call
        """
        try:
            renderer = self._renderers[format]
        except KeyError:
            raise ValueError(f"{format} is not a registered format.")
        return renderer

    @property
    def renderers(self):
        """
        Get a map of renderers.

        :return: map between file formats and renderers
        :rtype: dict
        """
        return self._renderers

    @property
    def supported_types(self):
        """
        Get a list of supported file formats.

        :return: List of supported file formats
        :rtype: list
        """
        return list(self.renderers.keys())


factory = RendererFactory()
factory.register("json", JsonRenderer)
factory.register("yaml", YamlRenderer)

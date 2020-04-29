import json
import yaml
from abc import ABC, abstractmethod


class BaseRenderer(ABC):
    @abstractmethod
    def render(self, data):
        pass


class JsonRenderer(BaseRenderer):
    def render(self, data):
        return json.dumps(data)


class YamlRenderer(BaseRenderer):
    def render(self, data):
        return yaml.dump(data)


class RendererFactory:
    def __init__(self):
        self._renderers = {}

    def register(self, format, renderer):
        self._renderers[format] = renderer

    def get_renderer(self, format):
        try:
            renderer = self._renderers[format]
        except KeyError:
            raise ValueError(f"{format} is not a valid format.")
        return renderer

    @property
    def renderers(self):
        return self._renderers

    @property
    def supported_types(self):
        return list(self.renderers.keys())


factory = RendererFactory()
factory.register("json", JsonRenderer)
factory.register("yaml", YamlRenderer)

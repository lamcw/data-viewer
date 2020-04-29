import pytest

from data_viewer.renderers import BaseRenderer, JsonRenderer, RendererFactory


@pytest.fixture
def renderer_factory():
    return RendererFactory()


def test_renderer_factory_register(renderer_factory):
    renderer_factory.register("test", BaseRenderer)
    renderer_factory.register("json", JsonRenderer)
    assert renderer_factory.renderers == {"test": BaseRenderer, "json": JsonRenderer}


def test_renderer_factory_get(renderer_factory):
    renderer_factory.register("json", JsonRenderer)
    assert renderer_factory.get_renderer("json") == JsonRenderer


def test_renderer_factory_get_invalid_format(renderer_factory):
    renderer_factory.register("json", JsonRenderer)
    with pytest.raises(ValueError):
        _ = renderer_factory.get_renderer("yaml")


def test_renderer_factory_supported_types(renderer_factory):
    renderer_factory.register("test", BaseRenderer)
    renderer_factory.register("json", JsonRenderer)
    assert sorted(renderer_factory.supported_types) == ["json", "test"]

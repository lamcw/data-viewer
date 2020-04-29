import pytest

from data_viewer.parsers import BaseParser, JsonParser, ParserFactory


@pytest.fixture
def parser_factory():
    return ParserFactory()


def test_parser_factory_register(parser_factory):
    parser_factory.register("test", BaseParser)
    parser_factory.register("json", JsonParser)
    assert parser_factory.parsers == {"test": BaseParser, "json": JsonParser}


def test_parser_factory_get(parser_factory):
    parser_factory.register("json", JsonParser)
    assert parser_factory.get_parser("json") == JsonParser


def test_parser_factory_get_invalid_format(parser_factory):
    parser_factory.register("json", JsonParser)
    with pytest.raises(ValueError):
        _ = parser_factory.get_parser("yaml")


def test_parser_factory_supported_types(parser_factory):
    parser_factory.register("test", BaseParser)
    parser_factory.register("json", JsonParser)
    assert sorted(parser_factory.supported_types) == ["json", "test"]

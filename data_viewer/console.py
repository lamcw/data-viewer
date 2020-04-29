"""Data viewer console driver."""
import argparse
import sys

from data_viewer.renderers import factory as renderer_factory
from data_viewer.parsers import factory as parser_factory
from data_viewer.serializers import PersonSerializer


def main():
    """Viewer's CLI driver."""
    arg_parser = argparse.ArgumentParser(
        description="View files in human-readable format."
    )
    arg_parser.add_argument(
        "file",
        metavar="FILE",
        default=sys.stdin,
        type=argparse.FileType(),
        nargs="*",
        help="If not supplied or '-', read from stdin",
    )
    arg_parser.add_argument(
        "-i",
        "--input-format",
        choices=parser_factory.supported_types,
        help="input format",
    )
    arg_parser.add_argument(
        "-o",
        "--output-format",
        choices=renderer_factory.supported_types,
        help="output format",
    )
    arg_parser.add_argument(
        "-l", "--list-support", action="store_true", help="list supported formats"
    )

    args = arg_parser.parse_args()

    if args.list_support:
        for t in parser_factory.supported_types:
            print(t)
        return

    PersonRenderer = renderer_factory.get_renderer(args.output_format)
    PersonParser = parser_factory.get_parser(args.input_format)
    renderer = PersonRenderer()
    parser = PersonParser()

    for file in args.file:
        with file as f:
            data = parser.parse(f.read())
            serializer = PersonSerializer(data=data)
            ppl = serializer.create()
            print("Python native data types:")
            print(ppl)
            print(f"{args.output_format}:")
            print(renderer.render(serializer.data))

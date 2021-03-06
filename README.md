# data-viewer
![CI](https://github.com/lamcw/data-viewer/workflows/CI/badge.svg?event=push)

`data-viewer` is a Python tool for serializing and deserializing data.

## Installation

Use [poetry](https://python-poetry.org/) to generate wheel and install with `pip`.

```console
$ poetry build -f wheel
Building data-viewer (0.1.0)
 - Building wheel
 - Built data_viewer-0.1.0-py3-none-any.whl
$ pip install dist/data_viewer-0.1.0-py3-none-any.whl
```

## Usage

```console
$ cat foo.json
[
  {
    "foo": "bar"
  }
]
$ data_viewer -i json -o yaml foo.json
- foo: bar
$ data_viewer -l  # list all supported file types
json
yaml
```

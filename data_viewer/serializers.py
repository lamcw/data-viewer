"""Serializer transforms data between native objects and python dict."""
import dataclasses
from abc import ABC, abstractmethod

import dacite

from data_viewer.person import Person


class BaseSerializer(ABC):
    """
    Base serializer that defines the interface of serializer.

    To serialize an object to native Python data types
    >>> foo = Foo(bar=1, var="string")
    >>> serializer = FooSerializer(foo)
    >>> serializer.data
    {"bar": 1, "var": "string"}

    To deserialize Python data types to Python object
    >>> foo = FooSerializer().create(data={"bar": 1, "var": "string"})
    >>> isintance(foo, Foo)
    True
    """

    def __init__(self, instance=None, data=None):  # noqa: D107
        self._instance = instance
        self._data = data

    @property
    def data(self):
        """
        Instance in Python dict.

        :rtype: dict
        """
        return self._data or vars(self._instance)

    @abstractmethod
    def create(self, data=None):
        """
        Create a new Python object from ``data``.

        :param data: object repr in dict or iterable containing dict of object
        :type data: iterable
        """
        pass


class PersonSerializer(BaseSerializer):
    """Serializer that specializes in serializing or deserializing :class:`Person`."""

    @property
    def data(self):
        """
        Get dict/list from :class:`Person` or iterable of :class:`Person`.

        :return: if serializer is instantiated with ``data``, ``data`` is returned,
                 list of dict is returned if ``instance`` is an iterable. If
                 ``instance`` is not an iterable but None instead, None is returned.
        """
        if self._data:
            return self._data

        try:
            return [dataclasses.asdict(person) for person in self._instance]
        except TypeError:
            # not iterable
            return (
                None if self._instance is None else dataclasses.asdict(self._instance)
            )

    def create(self, data=None):
        """
        Create objects from ``data``.

        :param data: optional, provided that ``data`` or ``instance`` is passed in
                     when instantiating the serializer
        :return: list of :class:`Person` if ``data`` is iterable, :class:`Person`
                 otherwise
        """
        d = data or self._data or self.data
        if d is None:
            raise ValueError("data required")
        try:
            return [dacite.from_dict(data_class=Person, data=p) for p in d]
        except TypeError:
            return dacite.from_dict(data_class=Person, data=d)

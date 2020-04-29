"""All implementations of serializers."""
import dataclasses
from abc import ABC, abstractmethod

import dacite

from data_viewer.person import Person


class BaseSerializer(ABC):
    def __init__(self, instance=None, data=None):
        self._instance = instance
        self._data = data

    @property
    def data(self):
        return self._data or vars(self._instance)

    @abstractmethod
    def create(self, data=None):
        pass


class PersonSerializer(BaseSerializer):
    @property
    def data(self):
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
        d = data or self._data or self.data
        if d is None:
            raise ValueError("data required")
        try:
            return [dacite.from_dict(data_class=Person, data=p) for p in d]
        except TypeError:
            return dacite.from_dict(data_class=Person, data=d)

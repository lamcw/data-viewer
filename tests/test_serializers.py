import pytest

import dataclasses
from data_viewer.person import Person
from data_viewer.serializers import BaseSerializer, PersonSerializer


@pytest.fixture
def simple_person():
    return Person(name="John Doe", address="123 foo st", phone_number="12345")


@pytest.fixture
def person_list():
    p1 = Person(name="John Doe", address="123 foo st", phone_number="12345")
    p2 = Person(name="Dion", address="5 bar drive", phone_number="00123499")
    return [p1, p2]


def test_base_serializer_abc():
    with pytest.raises(
        TypeError,
        match="Can't instantiate abstract class BaseSerializer with abstract "
        "methods create",
    ):
        _ = BaseSerializer()


def test_person_serializer_serialize(simple_person):
    serializer = PersonSerializer(simple_person)
    assert serializer.data == {
        "name": "John Doe",
        "address": "123 foo st",
        "phone_number": "12345",
    }


def test_person_serializer_empty_instance():
    serializer = PersonSerializer()
    assert serializer.data is None


def test_person_serializer_serialize_list(person_list):
    serializer = PersonSerializer(person_list)
    assert serializer.data == [
        {"name": "John Doe", "address": "123 foo st", "phone_number": "12345"},
        {"name": "Dion", "address": "5 bar drive", "phone_number": "00123499"},
    ]


def test_person_serializer_create(simple_person, person_list):
    with pytest.raises(ValueError):
        serializer = PersonSerializer()
        _ = serializer.create()
    assert simple_person == serializer.create(dataclasses.asdict(simple_person))
    assert person_list == serializer.create(
        [dataclasses.asdict(p) for p in person_list]
    )

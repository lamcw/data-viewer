"""Person class that all formats are going to be deserialized to."""
from dataclasses import dataclass


@dataclass
class Person:
    """Simple person class."""

    name: str
    address: str
    phone_number: str

#!/usr/bin/python3
"""Serialize and deserialize a custom object using pickle."""
import pickle


class CustomObject:
    """Class represents a custom object."""

    def __init__(self, name, age, is_student):
        self.name = name
        self.age = age
        self.is_student = is_student

    def display(self):
        print("Name: {}".format(self.name))
        print("Age: {}".format(self.age))
        print("Is Student: {}".format(self.is_student))

    def serialize(self, filename):
        try:
            with open(filename, "wb") as f:
                pickle.dump(self, f)
        except Exception:
            return None

    @classmethod
    def deserialize(cls, filename):
        """Load and return a CustomObject instance from the given file."""
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError, Exception):
            return None

#!/usr/bin/python3
"""Serialize and deserialize a dictionary using XML."""
import xml.etree.ElementTree as ET


def serialize_to_xml(dictionary, filename):
    """Serialize a dictionary to an XML file."""
    root = ET.Element("data")
    for key, value in dictionary.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    tree = ET.ElementTree(root)
    tree.write(filename)


def deserialize_from_xml(filename):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        data = {}
        for child in root:
            data[child.tag] = child.text
        return data
    except (FileNotFoundError, ET.ParseError):
        return None

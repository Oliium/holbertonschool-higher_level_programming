#!/usr/bin/python3
"""Convert CSV data to JSON format."""
import csv
import json


def convert_csv_to_json(filename):
    """Read a CSV file and write its content to data.json.

    Returns True on success, False if the file cannot be read.
    """
    try:
        with open(filename, "r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [row for row in reader]
        with open("data.json", "w", encoding="utf-8") as json_file:
            json.dump(rows, json_file)
        return True
    except (FileNotFoundError, OSError):
        return False

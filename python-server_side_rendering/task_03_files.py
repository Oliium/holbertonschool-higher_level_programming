#!/usr/bin/python3
"""A Flask application that displays product data from JSON or CSV files."""
import csv
import json
from flask import Flask, render_template, request

app = Flask(__name__)


def read_json(filename):
    """Read and return a list of products from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)


def read_csv(filename):
    """Read and return a list of products from a CSV file."""
    products = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['id'] = int(row['id'])
            row['price'] = float(row['price'])
            products.append(row)
    return products


@app.route('/products')
def products():
    """Display products from a JSON or CSV source, optionally filtered by id."""
    source = request.args.get('source')
    product_id = request.args.get('id')

    if source == 'json':
        data = read_json('products.json')
    elif source == 'csv':
        data = read_csv('products.csv')
    else:
        return render_template('product_display.html',
                               error="Wrong source")

    # Filter by id if one is provided
    if product_id is not None:
        data = [p for p in data if str(p['id']) == product_id]
        if not data:
            return render_template('product_display.html',
                                   error="Product not found")

    return render_template('product_display.html', products=data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

#!/usr/bin/python3
"""A Flask application that displays product data from JSON, CSV or SQLite."""
import csv
import json
import sqlite3
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


def read_sql(filename):
    """Read and return a list of products from a SQLite database."""
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, category, price FROM Products')
    rows = cursor.fetchall()
    conn.close()

    products = []
    for row in rows:
        products.append({
            'id': row[0],
            'name': row[1],
            'category': row[2],
            'price': row[3]
        })
    return products


@app.route('/products')
def products():
    """Display products from a JSON, CSV or SQL source, filtered by id."""
    source = request.args.get('source')
    product_id = request.args.get('id')

    try:
        if source == 'json':
            data = read_json('products.json')
        elif source == 'csv':
            data = read_csv('products.csv')
        elif source == 'sql':
            data = read_sql('products.db')
        else:
            return render_template('product_display.html',
                                   error="Wrong source")
    except Exception:
        return render_template('product_display.html',
                               error="Error reading data")

    # Filter by id if one is provided
    if product_id is not None:
        data = [p for p in data if str(p['id']) == product_id]
        if not data:
            return render_template('product_display.html',
                                   error="Product not found")

    return render_template('product_display.html', products=data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

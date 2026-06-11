#!/usr/bin/python3
"""Mini API maison avec le module standard http.server."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleAPIHandler(BaseHTTPRequestHandler):
    """Le portier qui répond selon la porte (le chemin) qu'on toque."""

    def do_GET(self):
        """Aiguille chaque chemin vers la bonne réponse."""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Hello, this is a simple API!")

        elif self.path == "/data":
            le_dico = {"name": "John", "age": 30, "city": "New York"}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(le_dico).encode("utf-8"))

        elif self.path == "/info":
            le_dico = {"version": "1.0",
                       "description": "A simple API built with http.server"}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(le_dico).encode("utf-8"))

        elif self.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Endpoint not found")


if __name__ == "__main__":
    mon_serveur = HTTPServer(("", 8000), SimpleAPIHandler)
    mon_serveur.serve_forever()

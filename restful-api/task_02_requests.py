#!/usr/bin/python3
"""Va chercher les posts sur JSONPlaceholder et en fait quelque chose."""
import csv
import requests


def fetch_and_print_posts():
    """Affiche le code de statut puis le titre de chaque post."""
    reponse = requests.get("https://jsonplaceholder.typicode.com/posts")
    print("Status Code: {}".format(reponse.status_code))

    if reponse.status_code == 200:
        les_posts = reponse.json()
        for post in les_posts:
            print(post["title"])


def fetch_and_save_posts():
    """Range id, title et body de chaque post dans un petit posts.csv."""
    reponse = requests.get("https://jsonplaceholder.typicode.com/posts")

    if reponse.status_code == 200:
        les_posts = reponse.json()

        mon_butin = []
        for post in les_posts:
            mon_butin.append({
                "id": post["id"],
                "title": post["title"],
                "body": post["body"],
            })

        with open("posts.csv", "w", newline="", encoding="utf-8") as fichier:
            stylo = csv.DictWriter(fichier, fieldnames=["id", "title", "body"])
            stylo.writeheader()
            stylo.writerows(mon_butin)

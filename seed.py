"""Vult de database met demomerken en 15 demokledingstukken.

Draaien:  .venv/bin/python seed.py
Bestaande merken (op naam) worden hergebruikt; kledingstukken worden
alleen toegevoegd als de tabel nog leeg is, tenzij je --force meegeeft.
"""

import sys

import db

MERKEN = [
    ("Levi's", "Verenigde Staten"),
    ("Nike", "Verenigde Staten"),
    ("Adidas", "Duitsland"),
    ("H&M", "Zweden"),
    ("Scotch & Soda", "Nederland"),
]

# (naam, categorie, maat, kleur, prijs, voorraad, merknaam)
KLEDING = [
    ("501 Original spijkerbroek", "Broek", "32", "Blauw", 109.95, 8, "Levi's"),
    ("Trucker jacket", "Jas", "L", "Lichtblauw", 129.95, 3, "Levi's"),
    ("Logo T-shirt", "Shirt", "M", "Wit", 24.95, 20, "Levi's"),
    ("Air Max 90", "Schoenen", "43", "Zwart", 149.99, 6, "Nike"),
    ("Dri-FIT hardloopshirt", "Shirt", "S", "Neon geel", 34.99, 15, "Nike"),
    ("Tech Fleece joggingbroek", "Broek", "M", "Grijs", 89.99, 9, "Nike"),
    ("Stan Smith sneakers", "Schoenen", "42", "Wit", 99.95, 11, "Adidas"),
    ("Trefoil hoodie", "Trui", "L", "Zwart", 69.95, 7, "Adidas"),
    ("Firebird trainingsjas", "Jas", "M", "Rood", 84.95, 4, "Adidas"),
    ("Gebreide trui", "Trui", "M", "Beige", 29.99, 25, "H&M"),
    ("Zomerjurk met bloemenprint", "Jurk", "38", "Blauw", 34.99, 12, "H&M"),
    ("Geplooide midi-rok", "Rok", "36", "Zwart", 27.99, 10, "H&M"),
    ("Slim fit chino", "Broek", "31", "Donkergroen", 99.95, 5, "Scotch & Soda"),
    ("Wollen overshirt", "Jas", "L", "Camel", 159.95, 2, "Scotch & Soda"),
    ("Linnen overhemd", "Shirt", "M", "Wit", 79.95, 0, "Scotch & Soda"),
]


def main(force=False):
    bestaand = {m["naam"]: m["merk_id"] for m in db.alle_merken()}
    for naam, land in MERKEN:
        if naam not in bestaand:
            bestaand[naam] = db.maak_merk(naam, land)["merk_id"]
            print(f"merk toegevoegd: {naam}")
    print(f"{len(bestaand)} merken aanwezig")

    if db.alle_kledingstukken() and not force:
        print("kledingstukken-tabel is niet leeg; sla seed over (gebruik --force om toch toe te voegen)")
        return
    for naam, cat, maat, kleur, prijs, voorraad, merk in KLEDING:
        db.maak_kledingstuk(naam, cat, maat, kleur, prijs, voorraad, bestaand[merk])
    print(f"{len(KLEDING)} kledingstukken toegevoegd")


if __name__ == "__main__":
    main(force="--force" in sys.argv)

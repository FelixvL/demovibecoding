"""Flask-API voor kledingstukken, opgeslagen in MySQL.

Verbindingsgegevens staan in .env (zie .env.example).
Starten:
    .venv/bin/python app.py
Draait op http://localhost:5001 en serveert ook de frontend uit ../fe
"""

import os

import mysql.connector
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import db

BASIS = os.path.dirname(os.path.abspath(__file__))
FRONTEND_MAP = os.path.join(os.path.dirname(BASIS), "fe")

app = Flask(__name__)
CORS(app)


@app.errorhandler(mysql.connector.Error)
def db_fout(e):
    return jsonify({"fout": f"Databasefout: {e}"}), 500


def lees_velden(bron):
    """Haal de kledingstukvelden uit form-data of JSON en valideer ze."""
    naam = (bron.get("naam") or "").strip()
    if not naam:
        return None, "Naam is verplicht"

    prijs_raw = str(bron.get("prijs") or "").strip().replace(",", ".")
    if not prijs_raw:
        return None, "Prijs is verplicht"
    try:
        prijs = round(float(prijs_raw), 2)
    except ValueError:
        return None, "Prijs is geen getal"

    voorraad_raw = str(bron.get("voorraad") or "0").strip()
    try:
        voorraad = int(voorraad_raw)
    except ValueError:
        return None, "Voorraad is geen geheel getal"

    return {
        "naam": naam,
        "categorie": (bron.get("categorie") or "").strip(),
        "maat": (bron.get("maat") or "").strip(),
        "kleur": (bron.get("kleur") or "").strip(),
        "prijs": prijs,
        "voorraad": voorraad,
    }, None


# --- API ----------------------------------------------------------------
@app.get("/api/kledingstukken")
def lijst():
    return jsonify(db.alle_kledingstukken())


@app.get("/api/kledingstukken/<int:item_id>")
def detail(item_id):
    item = db.kledingstuk_op_id(item_id)
    if item is None:
        return jsonify({"fout": "Niet gevonden"}), 404
    return jsonify(item)


@app.post("/api/kledingstukken")
def aanmaken():
    bron = request.get_json(silent=True) or request.form
    velden, fout = lees_velden(bron)
    if fout:
        return jsonify({"fout": fout}), 400
    item = db.maak_kledingstuk(**velden)
    return jsonify(item), 201


@app.delete("/api/kledingstukken/<int:item_id>")
def verwijderen(item_id):
    if not db.verwijder_kledingstuk(item_id):
        return jsonify({"fout": "Niet gevonden"}), 404
    return "", 204


# --- frontend -----------------------------------------------------------
@app.get("/")
def start():
    return send_from_directory(FRONTEND_MAP, "kleding.html")


@app.get("/<path:pagina>")
def frontend(pagina):
    return send_from_directory(FRONTEND_MAP, pagina)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

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
# Lokaal: de map ../fe (bron). Op Azure staat alleen be/ en gebruiken we de kopie in be/frontend.
_FE_BRON = os.path.join(os.path.dirname(BASIS), "fe")
FRONTEND_MAP = _FE_BRON if os.path.isdir(_FE_BRON) else os.path.join(BASIS, "frontend")

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

    merk_raw = str(bron.get("merk_id") or "").strip()
    merk_id = None
    if merk_raw:
        try:
            merk_id = int(merk_raw)
        except ValueError:
            return None, "merk_id is geen geheel getal"
        if db.merk_op_id(merk_id) is None:
            return None, "Merk bestaat niet"

    return {
        "naam": naam,
        "categorie": (bron.get("categorie") or "").strip(),
        "maat": (bron.get("maat") or "").strip(),
        "kleur": (bron.get("kleur") or "").strip(),
        "prijs": prijs,
        "voorraad": voorraad,
        "merk_id": merk_id,
    }, None


# --- API ----------------------------------------------------------------
@app.get("/api/kledingstukken")
def lijst():
    """Optioneel filteren met ?merk_id=3"""
    merk_id = request.args.get("merk_id", type=int)
    return jsonify(db.alle_kledingstukken(merk_id))


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


# --- merken -------------------------------------------------------------
@app.get("/api/merken")
def merken():
    return jsonify(db.alle_merken())


@app.get("/api/merken/<int:merk_id>")
def merk_detail(merk_id):
    merk = db.merk_op_id(merk_id)
    if merk is None:
        return jsonify({"fout": "Niet gevonden"}), 404
    return jsonify(merk)


@app.get("/api/merken/<int:merk_id>/kledingstukken")
def merk_kleding(merk_id):
    """Alle kledingstukken van één merk."""
    if db.merk_op_id(merk_id) is None:
        return jsonify({"fout": "Merk niet gevonden"}), 404
    return jsonify(db.alle_kledingstukken(merk_id))


@app.post("/api/merken")
def merk_aanmaken():
    bron = request.get_json(silent=True) or request.form
    naam = (bron.get("naam") or "").strip()
    if not naam:
        return jsonify({"fout": "Naam is verplicht"}), 400
    if any(m["naam"].lower() == naam.lower() for m in db.alle_merken()):
        return jsonify({"fout": "Merk bestaat al"}), 409
    return jsonify(db.maak_merk(naam, (bron.get("land") or "").strip())), 201


@app.delete("/api/merken/<int:merk_id>")
def merk_verwijderen(merk_id):
    if not db.verwijder_merk(merk_id):
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

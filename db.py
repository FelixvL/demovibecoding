"""Databaselaag voor kledingstukken (MySQL via mysql-connector-python).

Verbindingsgegevens komen uit .env (zie .env.example).
"""

import os
from decimal import Decimal

import mysql.connector
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME") or os.getenv("DATABASE") or "vibecodingdb",
    "charset": "utf8mb4",
    "autocommit": True,
}

# Azure Database for MySQL vereist TLS. Zet DB_SSL=true in .env.
if os.getenv("DB_SSL", "false").lower() in ("1", "true", "ja", "yes"):
    CONFIG["ssl_disabled"] = False
    CONFIG["ssl_verify_cert"] = True
else:
    CONFIG["ssl_disabled"] = True


def verbinding():
    return mysql.connector.connect(**CONFIG)


def _netjes(rij):
    """Maak een databaserij JSON-vriendelijk."""
    if rij is None:
        return None
    rij = dict(rij)
    if isinstance(rij.get("prijs"), Decimal):
        rij["prijs"] = float(rij["prijs"])
    return rij


def alle_kledingstukken():
    conn = verbinding()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM kledingstukken ORDER BY kledingstuk_id DESC")
        return [_netjes(r) for r in cur.fetchall()]
    finally:
        conn.close()


def kledingstuk_op_id(kledingstuk_id, conn=None):
    eigen = conn is None
    conn = conn or verbinding()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM kledingstukken WHERE kledingstuk_id = %s", (kledingstuk_id,))
        return _netjes(cur.fetchone())
    finally:
        if eigen:
            conn.close()


def maak_kledingstuk(naam, categorie, maat, kleur, prijs, voorraad=0):
    conn = verbinding()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO kledingstukken (naam, categorie, maat, kleur, prijs, voorraad) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (naam, categorie or None, maat or None, kleur or None, prijs, voorraad),
        )
        return kledingstuk_op_id(cur.lastrowid, conn)
    finally:
        conn.close()


def verwijder_kledingstuk(kledingstuk_id):
    conn = verbinding()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM kledingstukken WHERE kledingstuk_id = %s", (kledingstuk_id,))
        return cur.rowcount > 0
    finally:
        conn.close()


def maak_tabel():
    """Maakt de tabel aan als die nog niet bestaat (schema.sql)."""
    pad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
    with open(pad, encoding="utf-8") as f:
        sql = f.read()
    conn = verbinding()
    try:
        conn.cursor().execute(sql)
    finally:
        conn.close()

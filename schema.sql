-- Tabel zoals aangeleverd. Voer uit in de database uit DB_NAME.
CREATE TABLE IF NOT EXISTS kledingstukken (
    kledingstuk_id INT PRIMARY KEY AUTO_INCREMENT,
    naam VARCHAR(100) NOT NULL,
    categorie VARCHAR(50),
    maat VARCHAR(10),
    kleur VARCHAR(50),
    prijs DECIMAL(10,2) NOT NULL,
    voorraad INT DEFAULT 0
);

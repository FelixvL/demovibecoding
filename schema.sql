-- Merken
CREATE TABLE IF NOT EXISTS merken (
    merk_id INT PRIMARY KEY AUTO_INCREMENT,
    naam VARCHAR(100) NOT NULL UNIQUE,
    land VARCHAR(50)
);

-- Kledingstukken (zoals aangeleverd, plus merk_id)
CREATE TABLE IF NOT EXISTS kledingstukken (
    kledingstuk_id INT PRIMARY KEY AUTO_INCREMENT,
    naam VARCHAR(100) NOT NULL,
    categorie VARCHAR(50),
    maat VARCHAR(10),
    kleur VARCHAR(50),
    prijs DECIMAL(10,2) NOT NULL,
    voorraad INT DEFAULT 0,
    merk_id INT NULL,
    CONSTRAINT fk_kledingstuk_merk FOREIGN KEY (merk_id)
        REFERENCES merken(merk_id) ON DELETE SET NULL
);

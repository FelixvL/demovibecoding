-- Eenmalig uitvoeren op een bestaande database zonder merk_id-kolom
CREATE TABLE IF NOT EXISTS merken (
    merk_id INT PRIMARY KEY AUTO_INCREMENT,
    naam VARCHAR(100) NOT NULL UNIQUE,
    land VARCHAR(50)
);
ALTER TABLE kledingstukken
    ADD COLUMN merk_id INT NULL,
    ADD CONSTRAINT fk_kledingstuk_merk FOREIGN KEY (merk_id)
        REFERENCES merken(merk_id) ON DELETE SET NULL;

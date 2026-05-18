CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) UNIQUE NOT NULL,
    app_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id) ON DELETE CASCADE,
    review_text TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    identified_theme VARCHAR(50),
    source VARCHAR(50) DEFAULT 'Google Play Store'
);
INSERT INTO banks (bank_name, app_name) VALUES 
('Abyssinia', 'BoA Mobile'),
('CBE', 'CBE Mobile Banking'),
('Dashen', 'Dashen Bank') ON CONFLICT (bank_name) DO NOTHING;
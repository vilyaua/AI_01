-- Database initialization script for Spanish Learning App

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    native_language VARCHAR(10) NOT NULL CHECK (native_language IN ('en', 'ua')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vocabulary table
CREATE TABLE IF NOT EXISTS vocabulary (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    word_spanish VARCHAR(255) NOT NULL,
    word_native VARCHAR(255) NOT NULL,
    word_type VARCHAR(50) NOT NULL, -- 'noun', 'verb', 'adjective', 'adverb', etc.
    is_verb BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_reviewed TIMESTAMP,
    times_correct INTEGER DEFAULT 0,
    times_incorrect INTEGER DEFAULT 0
);

-- Verb conjugations table (for simple present tense)
CREATE TABLE IF NOT EXISTS verb_conjugations (
    id SERIAL PRIMARY KEY,
    vocabulary_id INTEGER REFERENCES vocabulary(id) ON DELETE CASCADE,
    yo VARCHAR(255) NOT NULL,
    tu VARCHAR(255) NOT NULL,
    el_ella_usted VARCHAR(255) NOT NULL,
    nosotros VARCHAR(255) NOT NULL,
    vosotros VARCHAR(255) NOT NULL,
    ellos_ellas_ustedes VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Learning sessions table
CREATE TABLE IF NOT EXISTS learning_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    vocabulary_id INTEGER REFERENCES vocabulary(id) ON DELETE CASCADE,
    user_answer TEXT,
    correct_answer TEXT,
    is_correct BOOLEAN,
    explanation TEXT,
    session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_vocabulary_user_id ON vocabulary(user_id);
CREATE INDEX IF NOT EXISTS idx_vocabulary_word_spanish ON vocabulary(word_spanish);
CREATE INDEX IF NOT EXISTS idx_verb_conjugations_vocabulary_id ON verb_conjugations(vocabulary_id);
CREATE INDEX IF NOT EXISTS idx_learning_sessions_user_id ON learning_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_sessions_vocabulary_id ON learning_sessions(vocabulary_id);


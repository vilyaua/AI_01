"""
Spanish Learning Application - Backend API
FastAPI backend for AI-driven Spanish learning app
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI
from io import BytesIO
from PIL import Image
import pytesseract
import speech_recognition as sr
from pydub import AudioSegment
import json

load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://spanish_user:spanish_pass@db:5432/spanish_learning")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# OpenAI setup
openai_api_key = os.getenv("OPENAI_API_KEY", "")
openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None

# Database Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    native_language = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    vocabulary = relationship("Vocabulary", back_populates="user")
    learning_sessions = relationship("LearningSession", back_populates="user")

class Vocabulary(Base):
    __tablename__ = "vocabulary"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    word_spanish = Column(String)
    word_native = Column(String)
    word_type = Column(String)
    is_verb = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_reviewed = Column(DateTime, nullable=True)
    times_correct = Column(Integer, default=0)
    times_incorrect = Column(Integer, default=0)
    user = relationship("User", back_populates="vocabulary")
    verb_conjugation = relationship("VerbConjugation", back_populates="vocabulary", uselist=False)
    learning_sessions = relationship("LearningSession", back_populates="vocabulary")

class VerbConjugation(Base):
    __tablename__ = "verb_conjugations"
    id = Column(Integer, primary_key=True, index=True)
    vocabulary_id = Column(Integer, ForeignKey("vocabulary.id"))
    yo = Column(String)
    tu = Column(String)
    el_ella_usted = Column(String)
    nosotros = Column(String)
    vosotros = Column(String)
    ellos_ellas_ustedes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    vocabulary = relationship("Vocabulary", back_populates="verb_conjugation")

class LearningSession(Base):
    __tablename__ = "learning_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vocabulary_id = Column(Integer, ForeignKey("vocabulary.id"))
    user_answer = Column(Text)
    correct_answer = Column(Text)
    is_correct = Column(Boolean)
    explanation = Column(Text)
    session_date = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="learning_sessions")
    vocabulary = relationship("Vocabulary", back_populates="learning_sessions")

Base.metadata.create_all(bind=engine)

# Pydantic Models
class UserCreate(BaseModel):
    username: str
    native_language: str

class UserResponse(BaseModel):
    id: int
    username: str
    native_language: str
    created_at: datetime

class VocabularyCreate(BaseModel):
    word_spanish: str
    word_native: str
    word_type: str

class VocabularyResponse(BaseModel):
    id: int
    word_spanish: str
    word_native: str
    word_type: str
    is_verb: bool
    created_at: datetime

class VerbConjugationResponse(BaseModel):
    yo: str
    tu: str
    el_ella_usted: str
    nosotros: str
    vosotros: str
    ellos_ellas_ustedes: str

class LearningQuestion(BaseModel):
    vocabulary_id: int
    question: str
    correct_answer: str

class LearningAnswer(BaseModel):
    vocabulary_id: int
    user_answer: str

class LearningResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str

# FastAPI app
app = FastAPI(title="Spanish Learning API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# AI Helper Functions
def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract text from image using OCR"""
    try:
        image = Image.open(BytesIO(image_bytes))
        text = pytesseract.image_to_string(image, lang='spa')
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

def extract_text_from_audio(audio_bytes: bytes) -> str:
    """Extract text from audio using speech recognition"""
    try:
        recognizer = sr.Recognizer()
        audio_file = BytesIO(audio_bytes)
        audio = AudioSegment.from_file(audio_file)
        wav_bytes = BytesIO()
        audio.export(wav_bytes, format="wav")
        wav_bytes.seek(0)
        
        with sr.AudioFile(wav_bytes) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='es-ES')
            return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing audio: {str(e)}")

def process_word_with_ai(word_text: str, native_language: str) -> dict:
    """Use OpenAI to process and extract word information"""
    if not openai_client:
        # Fallback if no API key
        return {
            "word_spanish": word_text,
            "word_native": "Translation needed",
            "word_type": "unknown",
            "is_verb": False
        }
    
    try:
        prompt = f"""Analyze this Spanish word/phrase and provide:
1. The Spanish word: {word_text}
2. Translation to {native_language}
3. Word type (noun, verb, adjective, adverb, etc.)
4. If it's a verb, indicate yes

Respond in JSON format:
{{
    "word_spanish": "word in Spanish",
    "word_native": "translation",
    "word_type": "type",
    "is_verb": true/false
}}"""
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Spanish language expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing error: {str(e)}")

def get_verb_conjugation(word: str) -> dict:
    """Get verb conjugation for simple present tense"""
    if not openai_client:
        return {
            "yo": word,
            "tu": word,
            "el_ella_usted": word,
            "nosotros": word,
            "vosotros": word,
            "ellos_ellas_ustedes": word
        }
    
    try:
        prompt = f"""Provide the simple present tense conjugation for the Spanish verb: {word}

Respond in JSON format:
{{
    "yo": "conjugation",
    "tu": "conjugation",
    "el_ella_usted": "conjugation",
    "nosotros": "conjugation",
    "vosotros": "conjugation",
    "ellos_ellas_ustedes": "conjugation"
}}"""
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Spanish grammar expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conjugation error: {str(e)}")

def check_answer_and_explain(user_answer: str, correct_answer: str, word_spanish: str, native_language: str) -> dict:
    """Check if answer is correct and provide explanation"""
    if not openai_client:
        is_correct = user_answer.lower().strip() == word_spanish.lower().strip()
        return {
            "is_correct": is_correct,
            "correct_answer": word_spanish,
            "explanation": "AI explanation not available without API key"
        }
    
    try:
        prompt = f"""The user is learning Spanish. They were asked to translate "{correct_answer}" from {native_language} to Spanish.
The correct answer is: {word_spanish}
The user answered: {user_answer}

Determine if the answer is correct (considering minor spelling variations). If incorrect, provide a helpful explanation.

Respond in JSON format:
{{
    "is_correct": true/false,
    "correct_answer": "{word_spanish}",
    "explanation": "helpful explanation in {native_language}"
}}"""
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Spanish teacher. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        # Fallback to simple comparison
        is_correct = user_answer.lower().strip() == word_spanish.lower().strip()
        return {
            "is_correct": is_correct,
            "correct_answer": word_spanish,
            "explanation": f"The correct answer is '{word_spanish}'. {'' if is_correct else 'Keep practicing!'}"
        }

# API Routes
@app.get("/")
def read_root():
    return {"message": "Spanish Learning API", "version": "1.0.0"}

@app.post("/api/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if user.native_language not in ['en', 'ua']:
        raise HTTPException(status_code=400, detail="Native language must be 'en' or 'ua'")
    
    db_user = User(username=user.username, native_language=user.native_language)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/api/vocabulary/{user_id}", response_model=VocabularyResponse)
def add_word_text(user_id: int, word: VocabularyCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    vocab = Vocabulary(
        user_id=user_id,
        word_spanish=word.word_spanish,
        word_native=word.word_native,
        word_type=word.word_type,
        is_verb=word.word_type.lower() == 'verb'
    )
    db.add(vocab)
    db.commit()
    db.refresh(vocab)
    
    # If verb, get conjugation
    if vocab.is_verb:
        conjugation_data = get_verb_conjugation(word.word_spanish)
        conjugation = VerbConjugation(
            vocabulary_id=vocab.id,
            **conjugation_data
        )
        db.add(conjugation)
        db.commit()
    
    return vocab

@app.post("/api/vocabulary/{user_id}/from-image")
def add_word_from_image(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    image_bytes = file.file.read()
    extracted_text = extract_text_from_image(image_bytes)
    
    if not extracted_text:
        raise HTTPException(status_code=400, detail="No text found in image")
    
    # Process with AI
    word_data = process_word_with_ai(extracted_text, user.native_language)
    
    vocab = Vocabulary(
        user_id=user_id,
        word_spanish=word_data["word_spanish"],
        word_native=word_data["word_native"],
        word_type=word_data["word_type"],
        is_verb=word_data.get("is_verb", False)
    )
    db.add(vocab)
    db.commit()
    db.refresh(vocab)
    
    if vocab.is_verb:
        conjugation_data = get_verb_conjugation(word_data["word_spanish"])
        conjugation = VerbConjugation(
            vocabulary_id=vocab.id,
            **conjugation_data
        )
        db.add(conjugation)
        db.commit()
    
    return vocab

@app.post("/api/vocabulary/{user_id}/from-audio")
def add_word_from_audio(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    audio_bytes = file.file.read()
    extracted_text = extract_text_from_audio(audio_bytes)
    
    if not extracted_text:
        raise HTTPException(status_code=400, detail="No text found in audio")
    
    # Process with AI
    word_data = process_word_with_ai(extracted_text, user.native_language)
    
    vocab = Vocabulary(
        user_id=user_id,
        word_spanish=word_data["word_spanish"],
        word_native=word_data["word_native"],
        word_type=word_data["word_type"],
        is_verb=word_data.get("is_verb", False)
    )
    db.add(vocab)
    db.commit()
    db.refresh(vocab)
    
    if vocab.is_verb:
        conjugation_data = get_verb_conjugation(word_data["word_spanish"])
        conjugation = VerbConjugation(
            vocabulary_id=vocab.id,
            **conjugation_data
        )
        db.add(conjugation)
        db.commit()
    
    return vocab

@app.get("/api/vocabulary/{user_id}", response_model=List[VocabularyResponse])
def get_vocabulary(user_id: int, db: Session = Depends(get_db)):
    vocab_list = db.query(Vocabulary).filter(Vocabulary.user_id == user_id).all()
    return vocab_list

@app.get("/api/vocabulary/{vocab_id}/conjugation", response_model=VerbConjugationResponse)
def get_conjugation(vocab_id: int, db: Session = Depends(get_db)):
    vocab = db.query(Vocabulary).filter(Vocabulary.id == vocab_id).first()
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")
    if not vocab.is_verb:
        raise HTTPException(status_code=400, detail="Word is not a verb")
    
    conjugation = db.query(VerbConjugation).filter(VerbConjugation.vocabulary_id == vocab_id).first()
    if not conjugation:
        # Generate conjugation on the fly
        conjugation_data = get_verb_conjugation(vocab.word_spanish)
        conjugation = VerbConjugation(
            vocabulary_id=vocab_id,
            **conjugation_data
        )
        db.add(conjugation)
        db.commit()
        db.refresh(conjugation)
    
    return conjugation

@app.get("/api/learning/{user_id}/question", response_model=LearningQuestion)
def get_learning_question(user_id: int, db: Session = Depends(get_db)):
    """Get a random word for learning session"""
    vocab = db.query(Vocabulary).filter(Vocabulary.user_id == user_id).first()
    if not vocab:
        raise HTTPException(status_code=404, detail="No vocabulary found for user")
    
    user = db.query(User).filter(User.id == user_id).first()
    question = f"Translate '{vocab.word_native}' to Spanish"
    
    return LearningQuestion(
        vocabulary_id=vocab.id,
        question=question,
        correct_answer=vocab.word_spanish
    )

@app.post("/api/learning/{user_id}/answer", response_model=LearningResponse)
def submit_answer(user_id: int, answer: LearningAnswer, db: Session = Depends(get_db)):
    """Submit answer and get feedback"""
    vocab = db.query(Vocabulary).filter(Vocabulary.id == answer.vocabulary_id).first()
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    # Check answer with AI
    result = check_answer_and_explain(
        answer.user_answer,
        vocab.word_native,
        vocab.word_spanish,
        user.native_language
    )
    
    # Update vocabulary stats
    if result["is_correct"]:
        vocab.times_correct += 1
    else:
        vocab.times_incorrect += 1
    vocab.last_reviewed = datetime.utcnow()
    
    # Save learning session
    session = LearningSession(
        user_id=user_id,
        vocabulary_id=answer.vocabulary_id,
        user_answer=answer.user_answer,
        correct_answer=vocab.word_spanish,
        is_correct=result["is_correct"],
        explanation=result["explanation"]
    )
    db.add(session)
    db.commit()
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


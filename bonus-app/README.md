# Spanish Learning Application - Bonus Project

AI-driven application for studying Spanish language for English and Ukrainian speaking users.

## Features

- ✅ Add words to vocabulary by:
  - **Text input**: Manual entry
  - **Voice/Audio**: Speech recognition
  - **Photo/Image**: OCR text extraction
- ✅ Learning mode with translation prompts (EN/UA → ES)
- ✅ Verb conjugation: All forms of simple present tense
- ✅ Error correction and AI-powered explanations
- ✅ Progress tracking (correct/incorrect answers)
- ✅ Multi-language support (English and Ukrainian)

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js (React/TypeScript)
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **AI Integration**: OpenAI API for:
  - Word processing and translation
  - Verb conjugation
  - Answer checking and explanations
- **OCR**: Tesseract for image text extraction
- **Speech Recognition**: Google Speech Recognition API

## Project Structure

```
bonus-app/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile           # Backend container
│   └── init.sql             # Database schema
├── frontend/
│   ├── pages/               # Next.js pages
│   ├── styles/              # CSS styles
│   ├── package.json         # Node dependencies
│   └── Dockerfile           # Frontend container
├── docker-compose.yml       # Multi-container setup
└── README.md                # This file
```

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key (optional, but recommended for full functionality)

## Setup Instructions

1. **Clone/Navigate to the project directory**
   ```bash
   cd bonus-app
   ```

2. **Set up environment variables**
   Create a `.env` file in the `bonus-app` directory (optional):
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Usage

1. **Create Account**
   - Enter username
   - Select native language (English or Ukrainian)

2. **Add Words**
   - **Text**: Enter Spanish word, translation, and type
   - **Image**: Upload image with Spanish text (OCR will extract it)
   - **Audio**: Upload audio file with Spanish pronunciation

3. **Learn**
   - Click "Start Learning" to begin practice
   - Translate words from your native language to Spanish
   - Get instant feedback with explanations
   - For verbs, see all conjugations in simple present tense

## API Endpoints

### Users
- `POST /api/users` - Create user
- `GET /api/users/{user_id}` - Get user

### Vocabulary
- `POST /api/vocabulary/{user_id}` - Add word (text)
- `POST /api/vocabulary/{user_id}/from-image` - Add word from image
- `POST /api/vocabulary/{user_id}/from-audio` - Add word from audio
- `GET /api/vocabulary/{user_id}` - Get all vocabulary

### Learning
- `GET /api/learning/{user_id}/question` - Get learning question
- `POST /api/learning/{user_id}/answer` - Submit answer

### Verb Conjugation
- `GET /api/vocabulary/{vocab_id}/conjugation` - Get verb conjugations

## Database Schema

- **users**: User accounts with native language
- **vocabulary**: Words and translations
- **verb_conjugations**: Simple present tense conjugations
- **learning_sessions**: Learning history and progress

## Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## Notes

- Without OpenAI API key, the app will work with limited functionality (basic word storage, simple answer checking)
- For full AI features (smart translations, conjugations, explanations), set `OPENAI_API_KEY` environment variable
- Image OCR requires Tesseract (included in Docker image)
- Audio processing requires internet connection for Google Speech Recognition

## Future Enhancements

- User authentication and sessions
- Spaced repetition algorithm
- Progress statistics and charts
- More verb tenses
- Pronunciation practice
- Mobile app version


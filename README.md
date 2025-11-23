# Module 1 Homework: Fundamentals of GenAI Tools

This project is part of the Ciklum AI course Module 1 homework, focusing on exploring and working with Generative AI tools.

## Project Overview

The homework consists of multiple steps exploring different aspects of GenAI:
- **Step 1**: Experimenting with local models using LM Studio
- **Step 2**: Building custom AI assistants (CustomGPT and GEM)
- **Step 3**: Recording walkthrough demonstrations
- **Step 4**: Submitting work
- **Bonus**: Building an AI-driven Spanish learning application

## Project Structure

```
AI_01/
├── README.md           # Project description and overview
├── ACTIVITY_LOG.md     # Detailed log of activities and time spent
├── NEXT_STEPS.md       # Planned steps and progress tracking
├── Homework.txt        # Original homework requirements
└── AGENTS.md           # Agent instructions and guidelines
```

## Requirements

### Step 1: Local Models (DevOps Perspective)
- Install LM Studio
- Download and test two models:
  - `gemma3-4b-it`
  - `llama-3.2-3b-instruct`
- Experiment with text and image inputs
- Document prompt variations and responses

### Step 2: Custom Assistants (Delivery Manager Perspective)
- Create CustomGPT in ChatGPT
- Create GEM in Gemini
- Upload documents and configure custom instructions
- Test and compare both assistants
- Prepare PoC for imaginary client

### Step 3: Demo Walkthrough (Delivery Manager Perspective)
- Record screen-sharing demo
- Show LM Studio interactions
- Show CustomGPT/GEM interactions
- Provide recommendations for demo scenarios

### Bonus: Spanish Learning Application (Full-Stack Developer Perspective)
- AI-driven application for learning Spanish
- Support for English and Ukrainian speaking users
- Docker-compose setup with database
- Features:
  - Add words via voice, text, or photo
  - Learning mode with translation prompts
  - Verb conjugation (simple present tense)
  - Error correction and explanations

## Technology Stack (Bonus)

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **AI Integration**: OpenAI API for language processing, translations, and explanations
- **Frontend**: Next.js (React/TypeScript)
- **OCR**: Tesseract for image text extraction
- **Speech Recognition**: Google Speech Recognition API

## Getting Started

1. Review `Homework.txt` for detailed requirements
2. Check `NEXT_STEPS.md` for current progress
3. Review `ACTIVITY_LOG.md` for completed work

### For Manual Steps (Steps 1-3):
- See `STEP1_GUIDE.md` for LM Studio setup
- See `STEP2_GUIDE.md` for CustomGPT/GEM creation
- See `STEP3_GUIDE.md` for demo walkthrough

### For Bonus Application:
- Navigate to `bonus-app/` directory
- See `bonus-app/README.md` for detailed setup and usage instructions
- Run `docker-compose up --build` to start the application

## Notes

- All documentation files are maintained and updated throughout the project
- Time tracking is maintained in `ACTIVITY_LOG.md`
- Progress is tracked in `NEXT_STEPS.md`


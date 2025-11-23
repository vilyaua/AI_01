# Quick Start Guide

This guide helps you quickly get started with the Module 1 Homework project.

## Project Overview

This project includes:
1. **Steps 1-3**: Manual tasks with guides (LM Studio, CustomGPT, GEM)
2. **Bonus**: Fully implemented Spanish Learning Application

## Quick Navigation

### For Manual Steps (Steps 1-4)

1. **Step 1 - LM Studio**:
   - Read: `STEP1_GUIDE.md`
   - Install LM Studio from https://lmstudio.ai
   - Download models: `gemma3-4b-it` and `llama-3.2-3b-instruct`
   - Test with text and images

2. **Step 2 - Custom Assistants**:
   - Read: `STEP2_GUIDE.md`
   - Create CustomGPT: https://chatgpt.com/gpts/editor
   - Create GEM: https://gemini.google.com/app
   - Test and compare both

3. **Step 3 - Demo Recording**:
   - Read: `STEP3_GUIDE.md` for recording instructions
   - Read: `STEP3_RECOMMENDATIONS.md` for demo scenarios
   - Record walkthrough (15-20 minutes)
   - Upload to Google Drive

4. **Step 4 - Submission**:
   - Create Google Drive folder (Name_Surname)
   - Upload video and transcript
   - Set permissions
   - Submit URLs

### For Bonus Application

1. **Navigate to application**:
   ```bash
   cd bonus-app
   ```

2. **Set up environment** (optional but recommended):
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_key_here" > .env
   ```

3. **Start the application**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

5. **Use the application**:
   - Create an account (username + native language)
   - Add words (text/image/audio)
   - Start learning!

## File Structure

```
AI_01/
├── README.md                    # Main project overview
├── ACTIVITY_LOG.md              # Time tracking and activities
├── NEXT_STEPS.md                # Progress tracking
├── Homework.txt                 # Original requirements
├── STEP1_GUIDE.md              # LM Studio guide
├── STEP2_GUIDE.md              # CustomGPT/GEM guide
├── STEP3_GUIDE.md              # Recording guide
├── STEP3_RECOMMENDATIONS.md    # Demo scenarios
├── QUICK_START.md              # This file
└── bonus-app/                  # Spanish Learning Application
    ├── README.md               # App documentation
    ├── docker-compose.yml      # Docker setup
    ├── backend/                # FastAPI backend
    └── frontend/               # Next.js frontend
```

## Prerequisites

### For Steps 1-3:
- Computer with internet connection
- ChatGPT Plus subscription (for CustomGPT) OR Google account (for GEM)
- Screen recording software
- Google Meet or similar for recording

### For Bonus Application:
- Docker and Docker Compose installed
- OpenAI API key (optional but recommended)
- 4GB+ RAM available for Docker containers

## Getting Help

- Check individual guide files for detailed instructions
- Review `README.md` for project overview
- Check `ACTIVITY_LOG.md` to see what's been completed
- Review `NEXT_STEPS.md` for current status

## Next Actions

1. ✅ Documentation created
2. ✅ Bonus application implemented
3. ⏳ Complete Step 1 (LM Studio testing)
4. ⏳ Complete Step 2 (CustomGPT/GEM creation)
5. ⏳ Complete Step 3 (Demo recording)
6. ⏳ Complete Step 4 (Submission)

Good luck with your homework! 🚀


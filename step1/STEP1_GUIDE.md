# Step 1: Local Models Guide (LM Studio)

## Overview
This guide helps you complete Step 1: experimenting with local models using LM Studio.

## Installation Steps

### ⚠️ For macOS Intel - Important Note

**LM Studio does NOT support Intel-based Macs.** It only works on Apple Silicon (M1/M2/M3/M4).

**Use Ollama instead** - it's the best alternative and works perfectly on Intel Macs!

#### Quick Ollama Setup:

1. **Install Ollama**:
   ```bash
   # If you have Homebrew:
   brew install ollama
   
   # Or download from: https://ollama.ai/download
   ```

2. **Start Ollama**:
   ```bash
   ollama serve
   ```
   (Keep this terminal running)

3. **Download Models** (in a new terminal):
   ```bash
   ollama pull gemma:2b
   ollama pull llama3.2:3b
   ```

4. **Test Models**:
   ```bash
   ollama run gemma:2b "What is AI?"
   ollama run llama3.2:3b "Explain machine learning"
   ```

5. **Use with Text Files**:
   ```bash
   cat your_file.txt | ollama run gemma:2b "Summarize this:"
   ```

**See `STEP1_MACOS_INTEL.md` for detailed instructions and alternatives!**

### For macOS Apple Silicon (M1/M2/M3/M4)

1. **Download LM Studio**
   - Visit: https://lmstudio.ai
   - Download the macOS version (labeled "M" for Apple Silicon)
   - The file will be a `.dmg` file

2. **Install LM Studio**
   - Open the downloaded `.dmg` file
   - Drag `LM Studio` to your Applications folder
   - Launch from Applications
   - Handle security warnings if needed

3. **Download Models**
   - Open LM Studio → "Search" or "Models" tab
   - Download: `gemma-2-2b-it` and `llama-3.2-3b-instruct`

## Testing Checklist

### Model 1: Gemma
- [ ] Load `gemma-2-2b-it` model (or `gemma3-4b-it` if available)
- [ ] Test with text file upload
- [ ] Test with image upload
- [ ] Try different prompt types:
  - [ ] Direct question
  - [ ] Creative writing prompt
  - [ ] Code generation prompt
  - [ ] Analysis prompt
- [ ] Document responses

### Model 2: Llama
- [ ] Load `llama-3.2-3b-instruct` model
- [ ] Test with text file upload
- [ ] Test with image upload
- [ ] Try same prompt types as Gemma
- [ ] Document responses

## Comparison Notes

Create a comparison document noting:
- Response quality differences
- Speed differences
- Context understanding
- Image processing capabilities
- Prompt sensitivity

## Test Files to Prepare

1. **Text File**: Create a sample document (e.g., technical documentation, article)
2. **Image File**: Prepare a test image (e.g., diagram, photo with text)

## Expected Outcomes

- Understanding of local model capabilities
- Comparison between two different models
- Insights into prompt engineering
- Documentation of findings


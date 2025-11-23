# Ollama Quick Start Guide for macOS Intel

Since LM Studio doesn't support Intel Macs, use Ollama instead. It's easy and works great!

## Installation (5 minutes)

### Step 1: Install Homebrew (if needed)

Open Terminal and run:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Ollama

```bash
brew install ollama
```

Or download from: https://ollama.ai/download

### Step 3: Start Ollama Server

```bash
ollama serve
```

**Keep this terminal window open!** The server needs to run in the background.

### Step 4: Download Models (New Terminal)

Open a **new terminal window** and run:

```bash
# Download Gemma model (~1.4GB)
ollama pull gemma:2b

# Download Llama model (~2GB)
ollama pull llama3.2:3b
```

This will take 5-15 minutes depending on your internet speed.

## Basic Usage

### Interactive Chat

```bash
# Start chat with Gemma
ollama run gemma:2b

# Then type your questions:
# > What is artificial intelligence?
# > Explain machine learning
# > Write a poem about coding
# Type /bye to exit
```

### One-off Questions

```bash
# Ask a single question
ollama run gemma:2b "What is the capital of France?"

# Ask Llama
ollama run llama3.2:3b "Explain quantum computing"
```

### Process Text Files

```bash
# Summarize a text file
cat document.txt | ollama run gemma:2b "Summarize this document:"

# Ask questions about a file
cat article.txt | ollama run llama3.2:3b "What are the main points?"
```

## For Your Homework

### Test Model 1: Gemma

```bash
# 1. Test with direct question
ollama run gemma:2b "What is artificial intelligence?"

# 2. Test with text file
cat your_document.txt | ollama run gemma:2b "Analyze this document"

# 3. Test creative writing
ollama run gemma:2b "Write a short story about a robot learning to paint"

# 4. Test code generation
ollama run gemma:2b "Write a Python function to calculate fibonacci numbers"
```

### Test Model 2: Llama

```bash
# Same tests with llama
ollama run llama3.2:3b "What is artificial intelligence?"
cat your_document.txt | ollama run llama3.2:3b "Summarize this"
ollama run llama3.2:3b "Write a poem about technology"
```

### Compare Responses

Run the same prompts on both models and note:
- Response quality
- Speed (time to respond)
- Creativity
- Accuracy
- Style differences

## Advanced: Web UI (Optional)

If you want a graphical interface like LM Studio:

```bash
# Install Open WebUI
brew install --cask open-webui

# Or use the web version
# Visit: https://github.com/open-webui/open-webui
```

## Tips

1. **Keep `ollama serve` running** in one terminal
2. **Use new terminals** for running models
3. **Models stay downloaded** - you only pull them once
4. **Fast responses** - Ollama is optimized and fast!
5. **Multiple models** - You can have many models installed

## Troubleshooting

### "Command not found: ollama"
- Make sure Homebrew installation completed
- Try: `brew install ollama` again
- Or download from https://ollama.ai

### "Connection refused"
- Make sure `ollama serve` is running
- Check the terminal where you started the server

### Slow responses
- This is normal for local models
- Smaller models (2b, 3b) are faster
- Close other applications to free up RAM

### Out of memory
- Use smaller models (2b instead of 7b)
- Close other applications
- Restart your Mac if needed

## Available Models

Popular models you can try:
- `gemma:2b` - Fast, good quality (recommended)
- `llama3.2:3b` - Balanced performance
- `mistral:7b` - Better quality, slower
- `phi:2.7b` - Microsoft's model
- `tinyllama:1.1b` - Very fast, lower quality

Pull any model with: `ollama pull model-name`

## Documentation

- Official docs: https://ollama.ai/docs
- GitHub: https://github.com/ollama/ollama
- Model library: https://ollama.ai/library

## For Your Homework Submission

When documenting your work:
- Note that you used Ollama instead of LM Studio
- Explain why (Intel Mac limitation)
- Show that you tested both models (gemma and llama)
- Compare the results
- This is perfectly acceptable for the assignment!


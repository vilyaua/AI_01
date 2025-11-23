# Step 1: Automated Model Testing Scripts

I've created automated scripts to help you test and compare both models easily!

## Available Scripts

### 1. `step1_test_models.py` - Standard Model Comparison

Tests both models with predefined prompts and generates a comparison report.

**Usage:**
```bash
python3 step1_test_models.py
```

**What it does:**
- Tests both `gemma:2b` and `llama3.2:3b` models
- Uses 5 different prompt types:
  - Direct questions
  - Creative writing
  - Code generation
  - Analysis
  - Complex reasoning
- Measures response times
- Generates a detailed comparison report
- Saves results to `step1_results/` directory

**Output:**
- JSON file with raw results
- Text report with side-by-side comparisons
- Summary statistics

### 2. `step1_test_with_file.py` - File Processing Comparison

Tests both models with a text file and asks questions about it.

**Usage:**
```bash
# With file path as argument
python3 step1_test_with_file.py path/to/your/file.txt

# Or run interactively
python3 step1_test_with_file.py
```

**What it does:**
- Reads a text file
- Asks both models questions about the file
- Compares their responses
- Generates a comparison report

**Example:**
```bash
python3 step1_test_with_file.py Homework.txt
```

## Prerequisites

1. **Ollama installed and running:**
   ```bash
   brew services start ollama
   # Or manually: ollama serve
   ```

2. **Models downloaded:**
   ```bash
   ollama pull gemma:2b
   ollama pull llama3.2:3b
   ```

3. **Python 3** (should be pre-installed on macOS)

## Quick Start

1. **Start Ollama server:**
   ```bash
   brew services start ollama
   ```

2. **Download models** (if not already done):
   ```bash
   ollama pull gemma:2b
   ollama pull llama3.2:3b
   ```

3. **Run the standard test:**
   ```bash
   python3 step1_test_models.py
   ```

4. **Check results:**
   ```bash
   ls -la step1_results/
   cat step1_results/comparison_report_*.txt
   ```

## What the Scripts Test

### Standard Test (`step1_test_models.py`)

1. **Direct Question**: "What is artificial intelligence?"
2. **Creative Writing**: "Write a short poem about technology and nature."
3. **Code Generation**: "Write a Python function to calculate the factorial of a number."
4. **Analysis**: "Explain the difference between machine learning and deep learning."
5. **Complex Reasoning**: Train speed comparison problem

### File Test (`step1_test_with_file.py`)

- You provide a text file
- You provide questions (or use defaults)
- Both models analyze the file and answer questions
- Responses are compared

## Output Files

All results are saved in `step1_results/` directory:

- `model_test_results_YYYYMMDD_HHMMSS.json` - Raw JSON data
- `comparison_report_YYYYMMDD_HHMMSS.txt` - Human-readable report
- `file_test_results_YYYYMMDD_HHMMSS.json` - File processing results
- `file_comparison_report_YYYYMMDD_HHMMSS.txt` - File comparison report

## Report Contents

The comparison reports include:

1. **Summary Statistics:**
   - Success rate
   - Total time
   - Average response time

2. **Detailed Comparisons:**
   - Side-by-side responses for each prompt
   - Response times
   - Full text of responses

3. **Analysis:**
   - Quality differences
   - Speed differences
   - Use case recommendations

## Tips

- **First run may be slow** - Models need to load into memory
- **Keep Ollama server running** - Don't close the terminal where `ollama serve` is running
- **Test with different files** - Try technical docs, articles, code, etc.
- **Review the reports** - They're perfect for your homework documentation

## Troubleshooting

### "Ollama not found"
- Make sure Ollama is installed: `brew install ollama`
- Check PATH: `which ollama`

### "Connection refused"
- Start Ollama server: `brew services start ollama`
- Or manually: `ollama serve` (keep terminal open)

### "Model not found"
- Download models: `ollama pull gemma:2b` and `ollama pull llama3.2:3b`
- Check available models: `ollama list`

### Script is slow
- This is normal - local models take 20-60 seconds per response
- Be patient, especially on Intel Macs

## For Your Homework

These scripts will help you:
- ✅ Test both models systematically
- ✅ Generate comparison data
- ✅ Create documentation-ready reports
- ✅ Save time on manual testing

Use the generated reports in your Step 1 documentation!


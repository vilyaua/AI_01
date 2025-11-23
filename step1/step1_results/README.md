# Step 1 Test Results

This directory contains the results from model comparison tests.

## Files Generated

- `model_test_results_YYYYMMDD_HHMMSS.json` - Raw JSON data from model tests
- `comparison_report_YYYYMMDD_HHMMSS.txt` - Human-readable comparison report
- `file_test_results_YYYYMMDD_HHMMSS.json` - Results from file processing tests
- `file_comparison_report_YYYYMMDD_HHMMSS.txt` - File processing comparison report

## Running the Tests

### Standard Model Comparison

```bash
python3 step1_test_models.py
```

This will:
- Test both Gemma and Llama models with 5 different prompt types
- Measure response times
- Generate a comparison report
- Save results to this directory

### File Processing Comparison

```bash
python3 step1_test_with_file.py path/to/your/file.txt
```

Or run interactively:
```bash
python3 step1_test_with_file.py
```

This will:
- Process a text file with both models
- Ask questions about the file
- Compare responses
- Generate a comparison report

## Prerequisites

1. Ollama installed and running
2. Models downloaded:
   ```bash
   ollama pull gemma:2b
   ollama pull llama3.2:3b
   ```

## Notes

- Tests may take 5-15 minutes depending on your system
- Make sure Ollama server is running: `ollama serve` or `brew services start ollama`
- Results are saved with timestamps for easy tracking


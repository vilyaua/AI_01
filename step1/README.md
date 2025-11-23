# Step 1: Local Models Testing

This folder contains all materials and tools for completing Step 1 of the homework.

## Contents

### 📚 Documentation
- **`STEP1_GUIDE.md`** - General guide for Step 1 (all platforms)
- **`STEP1_MACOS_INTEL.md`** - Detailed guide for macOS Intel users (Ollama setup)
- **`STEP1_TESTING.md`** - Guide for using the automated testing scripts
- **`OLLAMA_QUICK_START.md`** - Quick start guide for Ollama

### 🧪 Testing Scripts
- **`step1_test_models.py`** - Main comparison script (tests both models with predefined prompts)
- **`step1_test_with_file.py`** - File processing script (tests models with your text files)
- **`run_tests.sh`** - Interactive launcher script

### 📊 Results
- **`step1_results/`** - Directory where test results and reports are saved

## Quick Start

### 1. Install Ollama (if not done)
```bash
brew install ollama
brew services start ollama
```

### 2. Download Models
```bash
ollama pull gemma:2b
ollama pull llama3.2:3b
```

### 3. Run Tests

**Option A: Use the launcher script**
```bash
cd step1
./run_tests.sh
```

**Option B: Run directly**
```bash
cd step1
python3 step1_test_models.py
```

**Option C: Test with a file**
```bash
cd step1
python3 step1_test_with_file.py ../Homework.txt
```

## What Gets Tested

The `step1_test_models.py` script tests both models with:
1. Direct questions
2. Creative writing prompts
3. Code generation
4. Analysis tasks
5. Complex reasoning

## Output

All results are saved in `step1_results/`:
- JSON files with raw data
- Text reports with side-by-side comparisons
- Summary statistics

## File Structure

```
step1/
├── README.md                    # This file
├── STEP1_GUIDE.md              # General guide
├── STEP1_MACOS_INTEL.md        # Intel Mac specific
├── STEP1_TESTING.md            # Testing guide
├── OLLAMA_QUICK_START.md       # Ollama quick start
├── step1_test_models.py        # Main test script
├── step1_test_with_file.py     # File test script
├── run_tests.sh                # Launcher script
└── step1_results/              # Test results directory
    └── README.md               # Results documentation
```

## Notes

- Make sure Ollama server is running before testing
- Tests may take 5-15 minutes depending on your system
- Results are timestamped for easy tracking
- All scripts work from within this directory

## For Your Homework

Use the generated comparison reports in your Step 1 submission. The reports include:
- Response quality comparisons
- Speed measurements
- Detailed side-by-side analysis
- Summary statistics

Perfect for documenting your findings!


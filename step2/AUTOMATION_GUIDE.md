# Step 2: Automation Guide

This guide explains how to automate testing and comparison of CustomGPT and GEM assistants.

## Options for Automation

### Option 1: API-Based Automation (Recommended if APIs are available)

**Pros:**
- Fully automated
- Fast and reliable
- Easy to repeat tests

**Cons:**
- Requires API access
- May need API keys
- CustomGPT may not have direct API

**Setup:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run automated test
python3 step2_test_assistants.py
```

**API Setup:**
1. **For GEM (Gemini)**:
   - Get API key from: https://makersuite.google.com/app/apikey
   - Set as environment variable or enter when prompted

2. **For CustomGPT**:
   - May need OpenAI API key
   - Or use browser automation (see Option 2)

### Option 2: Manual Testing with Template (Easiest)

**Pros:**
- Works with any setup
- No API keys needed
- Structured approach

**Cons:**
- Requires manual copy-paste
- Takes more time

**Usage:**
```bash
python3 manual_testing_template.py
```

The script will:
1. Guide you through each question
2. Prompt you to test in CustomGPT and GEM
3. Let you paste responses
4. Generate comparison reports automatically

### Option 3: Browser Automation (Advanced)

**Pros:**
- Fully automated
- Works with web interfaces

**Cons:**
- Complex setup
- May break if UI changes
- Requires browser automation tools

**Setup:**
```bash
# Install Playwright
pip install playwright
playwright install

# Or Selenium
pip install selenium
```

**Note:** Browser automation scripts are not included but can be created if needed.

## Recommended Approach

### For Quick Testing: Use Manual Template

1. Run `python3 manual_testing_template.py`
2. Follow the prompts
3. Copy responses from both assistants
4. Get automated comparison report

### For Repeated Testing: Use API (if available)

1. Set up API keys
2. Run `python3 step2_test_assistants.py`
3. Get fully automated results

## File Structure

```
step2/
├── step2_test_assistants.py      # API-based automation
├── manual_testing_template.py    # Manual testing helper
├── requirements.txt               # Python dependencies
├── AUTOMATION_GUIDE.md           # This file
├── test_questions.md             # Test questions
└── step2_results/                 # Generated reports
    ├── assistant_test_results_*.json
    ├── comparison_report_*.txt
    └── manual_test_results_*.json
```

## Example Workflow

### Using Manual Template

```bash
# 1. Start the script
python3 manual_testing_template.py

# 2. For each question:
#    - Script shows the question
#    - You test in CustomGPT, copy response
#    - You test in GEM, copy response
#    - Enter comparison notes
#    - Continue to next question

# 3. Script generates:
#    - JSON file with all results
#    - Text report with comparisons
```

### Using API Automation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get API keys
#    - Gemini: https://makersuite.google.com/app/apikey
#    - OpenAI: https://platform.openai.com/api-keys

# 3. Run test
python3 step2_test_assistants.py

# 4. Enter API keys when prompted

# 5. Script automatically:
#    - Tests both assistants
#    - Generates comparison reports
```

## Output Files

### JSON Results
Contains structured data:
- Questions asked
- Responses from both assistants
- Timing information
- Comparison notes

### Text Reports
Human-readable comparison:
- Summary statistics
- Side-by-side responses
- Comparison analysis

## Tips

1. **Start with Manual Template**: Easiest way to get started
2. **Test a Few Questions First**: Don't test all 18 questions at once
3. **Save Your Work**: Results are automatically saved
4. **Review Reports**: Check the generated reports for insights
5. **Iterate**: Run tests multiple times to refine comparisons

## Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key invalid"
- Check API key is correct
- Ensure API is enabled
- Check rate limits

### "No responses"
- Verify assistants are set up correctly
- Check knowledge base documents are uploaded
- Ensure custom instructions are configured

## Next Steps

After running tests:
1. Review comparison reports
2. Document key findings
3. Complete comparison matrix in STEP2_GUIDE.md
4. Prepare PoC presentation materials


#!/bin/bash
# Quick script to run Step 1 model tests

echo "=========================================="
echo "Step 1: Model Comparison Tests"
echo "=========================================="
echo ""

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠ Warning: Ollama server may not be running"
    echo "Start it with: brew services start ollama"
    echo "Or: ollama serve"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Choose test type:"
echo "1) Standard model comparison (5 predefined prompts)"
echo "2) File processing comparison (custom file)"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "Running standard model comparison..."
        python3 step1_test_models.py
        ;;
    2)
        echo ""
        read -p "Enter path to text file: " filepath
        if [ -f "$filepath" ]; then
            python3 step1_test_with_file.py "$filepath"
        else
            echo "Error: File not found: $filepath"
            exit 1
        fi
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Tests complete! Check step1_results/ for output"
echo "=========================================="


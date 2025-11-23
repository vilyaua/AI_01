#!/usr/bin/env python3
"""
Model Comparison Script with File Input
Tests both models with a text file and compares their analysis.
"""

import subprocess
import json
import time
from datetime import datetime
from pathlib import Path
import sys

# Configuration
MODELS = {
    "gemma": "gemma:2b",
    "llama": "llama3.2:3b"
}

def check_ollama_installed():
    """Check if Ollama is installed and accessible."""
    try:
        subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("✗ Error: Ollama is not installed or not in PATH")
        print("  Install it with: brew install ollama")
        return False

def process_file_with_model(model_name, file_path, questions):
    """Process a file with a model and ask questions about it."""
    print(f"\n{'='*60}")
    print(f"Processing with: {model_name}")
    print(f"{'='*60}")
    
    results = {
        "model_name": model_name,
        "file_path": str(file_path),
        "test_time": datetime.now().isoformat(),
        "responses": []
    }
    
    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return None
    
    print(f"File: {file_path.name} ({len(file_content)} characters)")
    
    # Process each question
    for i, question in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] Question: {question}")
        print("  Processing...", end=" ", flush=True)
        
        # Combine file content with question
        prompt = f"{file_content}\n\nQuestion: {question}"
        
        start_time = time.time()
        try:
            result = subprocess.run(
                ["ollama", "run", model_name, prompt],
                capture_output=True,
                text=True,
                timeout=180
            )
            
            elapsed_time = time.time() - start_time
            
            if result.returncode == 0:
                response = result.stdout.strip()
                print(f"✓ ({elapsed_time:.1f}s)")
                
                results["responses"].append({
                    "question": question,
                    "response": response,
                    "time_seconds": elapsed_time,
                    "success": True
                })
            else:
                print(f"✗ Error")
                results["responses"].append({
                    "question": question,
                    "response": None,
                    "time_seconds": elapsed_time,
                    "success": False,
                    "error": result.stderr
                })
        except subprocess.TimeoutExpired:
            elapsed_time = time.time() - start_time
            print(f"✗ Timeout")
            results["responses"].append({
                "question": question,
                "response": None,
                "time_seconds": elapsed_time,
                "success": False,
                "error": "Timeout"
            })
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"✗ Exception: {e}")
            results["responses"].append({
                "question": question,
                "response": None,
                "time_seconds": elapsed_time,
                "success": False,
                "error": str(e)
            })
        
        time.sleep(1)  # Small delay between queries
    
    return results

def generate_file_comparison_report(all_results, file_path):
    """Generate a comparison report for file processing."""
    report = []
    report.append("="*80)
    report.append("FILE PROCESSING COMPARISON REPORT")
    report.append("="*80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"File: {file_path}")
    report.append("")
    
    # Summary
    report.append("SUMMARY")
    report.append("-"*80)
    
    for result in all_results:
        if result is None:
            continue
        
        successful = sum(1 for r in result["responses"] if r["success"])
        total_time = sum(r["time_seconds"] for r in result["responses"])
        avg_time = total_time / len(result["responses"]) if result["responses"] else 0
        
        report.append(f"\n{result['model_name']}:")
        report.append(f"  Successful: {successful}/{len(result['responses'])}")
        report.append(f"  Total time: {total_time:.2f}s")
        report.append(f"  Average time: {avg_time:.2f}s")
    
    # Detailed responses
    report.append("\n" + "="*80)
    report.append("DETAILED RESPONSES")
    report.append("="*80)
    
    if all_results and all_results[0]:
        num_questions = len(all_results[0]["responses"])
        
        for q_idx in range(num_questions):
            question = all_results[0]["responses"][q_idx]["question"]
            report.append(f"\n{'='*80}")
            report.append(f"QUESTION {q_idx + 1}: {question}")
            report.append(f"{'='*80}")
            
            for result in all_results:
                if result is None:
                    continue
                
                response_data = result["responses"][q_idx]
                report.append(f"\n{result['model_name']}:")
                report.append(f"  Time: {response_data['time_seconds']:.2f}s")
                
                if response_data['success']:
                    response = response_data['response']
                    if len(response) > 1000:
                        response = response[:1000] + "... [truncated]"
                    report.append(f"  Response:\n    {response.replace(chr(10), chr(10) + '    ')}")
                else:
                    report.append(f"  Error: {response_data.get('error', 'Unknown error')}")
            
            report.append("")
    
    return "\n".join(report)

def main():
    """Main function."""
    print("="*80)
    print("FILE PROCESSING COMPARISON TEST")
    print("="*80)
    
    # Check Ollama
    if not check_ollama_installed():
        sys.exit(1)
    
    # Get file path
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    else:
        file_path_str = input("\nEnter path to text file to test: ").strip()
        file_path = Path(file_path_str)
    
    if not file_path.exists():
        print(f"✗ Error: File not found: {file_path}")
        sys.exit(1)
    
    # Get questions
    print("\nEnter questions to ask about the file (press Enter on empty line to finish):")
    questions = []
    while True:
        question = input(f"Question {len(questions) + 1}: ").strip()
        if not question:
            break
        questions.append(question)
    
    if not questions:
        # Default questions
        questions = [
            "Summarize the main points of this document.",
            "What are the key concepts discussed?",
            "What is the main conclusion or takeaway?"
        ]
        print(f"\nUsing default questions: {questions}")
    
    # Test both models
    all_results = []
    
    for model_key, model_name in MODELS.items():
        result = process_file_with_model(model_name, file_path, questions)
        all_results.append(result)
    
    # Generate report
    print("\n" + "="*80)
    print("GENERATING COMPARISON REPORT")
    print("="*80)
    
    report = generate_file_comparison_report(all_results, file_path)
    
    # Print report
    print("\n" + report)
    
    # Save to files
    output_dir = Path("step1_results")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    json_file = output_dir / f"file_test_results_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    report_file = output_dir / f"file_comparison_report_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✓ Results saved to: {json_file}")
    print(f"✓ Report saved to: {report_file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


#!/usr/bin/env python3
"""
Model Comparison Script for Step 1
Tests both Gemma and Llama models with the same prompts and generates a comparison report.
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

# Test prompts
TEST_PROMPTS = [
    {
        "category": "Direct Question",
        "prompt": "What is artificial intelligence?"
    },
    {
        "category": "Creative Writing",
        "prompt": "Write a short poem about technology and nature."
    },
    {
        "category": "Code Generation",
        "prompt": "Write a Python function to calculate the factorial of a number."
    },
    {
        "category": "Analysis",
        "prompt": "Explain the difference between machine learning and deep learning."
    },
    {
        "category": "Complex Reasoning",
        "prompt": "If a train travels 120 km in 2 hours, and another train travels 180 km in 3 hours, which train is faster?"
    }
]

def check_ollama_installed():
    """Check if Ollama is installed and accessible."""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ Ollama found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("✗ Error: Ollama is not installed or not in PATH")
        print("  Install it with: brew install ollama")
        return False
    except Exception as e:
        print(f"✗ Error checking Ollama: {e}")
        return False
    return False

def check_model_available(model_name):
    """Check if a model is available locally."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if model_name in result.stdout:
            return True
    except Exception as e:
        print(f"  Warning: Could not check model availability: {e}")
    return False

def run_ollama_query(model, prompt, timeout=120):
    """Run a query against Ollama and return the response."""
    print(f"  Querying {model}...", end=" ", flush=True)
    start_time = time.time()
    
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            response = result.stdout.strip()
            print(f"✓ ({elapsed_time:.1f}s)")
            return {
                "success": True,
                "response": response,
                "time_seconds": elapsed_time,
                "error": None
            }
        else:
            print(f"✗ Error: {result.stderr}")
            return {
                "success": False,
                "response": None,
                "time_seconds": elapsed_time,
                "error": result.stderr
            }
    except subprocess.TimeoutExpired:
        elapsed_time = time.time() - start_time
        print(f"✗ Timeout after {elapsed_time:.1f}s")
        return {
            "success": False,
            "response": None,
            "time_seconds": elapsed_time,
            "error": "Timeout"
        }
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"✗ Exception: {e}")
        return {
            "success": False,
            "response": None,
            "time_seconds": elapsed_time,
            "error": str(e)
        }

def test_model(model_key, model_name, prompts):
    """Test a model with all prompts."""
    print(f"\n{'='*60}")
    print(f"Testing Model: {model_name} ({model_key})")
    print(f"{'='*60}")
    
    # Check if model is available
    if not check_model_available(model_name):
        print(f"⚠ Warning: Model {model_name} may not be downloaded.")
        print(f"  Download it with: ollama pull {model_name}")
        response = input("  Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return None
    
    results = {
        "model_key": model_key,
        "model_name": model_name,
        "test_time": datetime.now().isoformat(),
        "prompts": []
    }
    
    for i, test_case in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] {test_case['category']}: {test_case['prompt'][:50]}...")
        
        result = run_ollama_query(model_name, test_case['prompt'])
        
        results["prompts"].append({
            "category": test_case['category'],
            "prompt": test_case['prompt'],
            "result": result
        })
        
        # Small delay between queries
        time.sleep(1)
    
    return results

def generate_comparison_report(all_results):
    """Generate a comparison report."""
    report = []
    report.append("="*80)
    report.append("MODEL COMPARISON REPORT")
    report.append("="*80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Summary statistics
    report.append("SUMMARY STATISTICS")
    report.append("-"*80)
    
    for model_result in all_results:
        if model_result is None:
            continue
        
        successful = sum(1 for p in model_result["prompts"] if p["result"]["success"])
        total_time = sum(p["result"]["time_seconds"] for p in model_result["prompts"])
        avg_time = total_time / len(model_result["prompts"]) if model_result["prompts"] else 0
        
        report.append(f"\n{model_result['model_name']}:")
        report.append(f"  Successful queries: {successful}/{len(model_result['prompts'])}")
        report.append(f"  Total time: {total_time:.2f}s")
        report.append(f"  Average time per query: {avg_time:.2f}s")
    
    # Detailed comparisons
    report.append("\n" + "="*80)
    report.append("DETAILED COMPARISONS")
    report.append("="*80)
    
    # Group by prompt category
    for i, test_case in enumerate(TEST_PROMPTS):
        report.append(f"\n{'='*80}")
        report.append(f"PROMPT {i+1}: {test_case['category']}")
        report.append(f"{'='*80}")
        report.append(f"Prompt: {test_case['prompt']}")
        report.append("")
        
        for model_result in all_results:
            if model_result is None:
                continue
            
            prompt_result = model_result["prompts"][i]
            result = prompt_result["result"]
            
            report.append(f"\n{model_result['model_name']}:")
            report.append(f"  Time: {result['time_seconds']:.2f}s")
            
            if result['success']:
                response = result['response']
                # Truncate very long responses
                if len(response) > 500:
                    response = response[:500] + "... [truncated]"
                report.append(f"  Response:\n    {response.replace(chr(10), chr(10) + '    ')}")
            else:
                report.append(f"  Error: {result['error']}")
        
        report.append("")
    
    return "\n".join(report)

def save_results(all_results, report):
    """Save results to files."""
    output_dir = Path("step1_results")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON results
    json_file = output_dir / f"model_test_results_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Results saved to: {json_file}")
    
    # Save comparison report
    report_file = output_dir / f"comparison_report_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ Report saved to: {report_file}")
    
    return json_file, report_file

def main():
    """Main function."""
    print("="*80)
    print("MODEL COMPARISON TEST SCRIPT")
    print("="*80)
    print("\nThis script will test both models with the same prompts")
    print("and generate a comparison report.\n")
    
    # Check Ollama installation
    if not check_ollama_installed():
        sys.exit(1)
    
    # Check if Ollama server is running
    print("\nChecking Ollama server...")
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ Ollama server is running")
        else:
            print("⚠ Ollama server may not be running")
            print("  Start it with: ollama serve")
            response = input("  Continue anyway? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)
    except Exception:
        print("⚠ Could not verify Ollama server status")
        print("  Make sure Ollama server is running: ollama serve")
        response = input("  Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Test both models
    all_results = []
    
    for model_key, model_name in MODELS.items():
        results = test_model(model_key, model_name, TEST_PROMPTS)
        all_results.append(results)
    
    # Generate report
    print("\n" + "="*80)
    print("GENERATING COMPARISON REPORT")
    print("="*80)
    
    report = generate_comparison_report(all_results)
    
    # Print report to console
    print("\n" + report)
    
    # Save to files
    json_file, report_file = save_results(all_results, report)
    
    print("\n" + "="*80)
    print("TESTING COMPLETE!")
    print("="*80)
    print(f"\nResults saved in: step1_results/")
    print(f"  - JSON data: {json_file.name}")
    print(f"  - Text report: {report_file.name}")
    print("\nYou can use these files for your homework submission!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


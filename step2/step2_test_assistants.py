#!/usr/bin/env python3
"""
Step 2: Automated Testing Script for CustomGPT and GEM
Tests both assistants with the same questions and generates comparison reports.

Note: This script requires manual API setup or browser automation.
See README.md for setup instructions.
"""

import json
import time
from datetime import datetime
from pathlib import Path
import sys

# Try importing API clients (install if needed)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠ OpenAI library not installed. Install with: pip install openai")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠ Google Generative AI library not installed. Install with: pip install google-generativeai")

# Configuration
TEST_QUESTIONS_FILE = Path(__file__).parent / "test_questions.md"
OUTPUT_DIR = Path(__file__).parent / "step2_results"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load test questions
def load_test_questions():
    """Load test questions from test_questions.md"""
    questions = []
    try:
        with open(TEST_QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse questions from markdown
        lines = content.split('\n')
        current_question = None
        current_category = None
        
        for line in lines:
            if line.startswith('## Category'):
                current_category = line.replace('## Category', '').strip()
            elif line.startswith('### Question'):
                if current_question:
                    questions.append(current_question)
                current_question = {
                    'category': current_category,
                    'number': line.replace('### Question', '').strip(),
                    'question': '',
                    'expected_topics': []
                }
            elif line.startswith('**Question**:'):
                if current_question:
                    current_question['question'] = line.replace('**Question**:', '').strip()
            elif line.startswith('**Expected Topics**:'):
                # Next lines until next question are expected topics
                pass
            elif current_question and line.strip() and not line.startswith('**'):
                if line.strip().startswith('-'):
                    current_question['expected_topics'].append(line.strip())
        
        if current_question:
            questions.append(current_question)
    except Exception as e:
        print(f"⚠ Error loading questions: {e}")
        # Fallback to default questions
        questions = get_default_questions()
    
    return questions

def get_default_questions():
    """Default test questions if file can't be loaded"""
    return [
        {
            'category': 'Basic Concepts',
            'number': '1',
            'question': 'What is machine learning and how does it differ from traditional programming?',
            'expected_topics': []
        },
        {
            'category': 'Company and Services',
            'number': '4',
            'question': 'What services does TechSolutions Inc. offer and which would be best for a retail company?',
            'expected_topics': []
        },
        {
            'category': 'Implementation',
            'number': '7',
            'question': "I'm planning to implement an AI solution. What are the key steps I should follow?",
            'expected_topics': []
        }
    ]

def query_customgpt_api(question, api_key, assistant_id=None):
    """
    Query CustomGPT using OpenAI API
    Note: CustomGPT may require specific setup. Check OpenAI documentation.
    """
    if not OPENAI_AVAILABLE:
        return None, "OpenAI library not available"
    
    try:
        client = OpenAI(api_key=api_key)
        
        # For CustomGPT, you might need to use the assistant API
        # This is a template - adjust based on actual API
        response = client.chat.completions.create(
            model="gpt-4",  # Adjust based on your CustomGPT setup
            messages=[
                {"role": "system", "content": "You are an AI consultant assistant."},
                {"role": "user", "content": question}
            ],
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        return answer, None
    except Exception as e:
        return None, str(e)

def query_gem_api(question, api_key):
    """
    Query GEM using Google Generative AI API
    """
    if not GEMINI_AVAILABLE:
        return None, "Google Generative AI library not available"
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(question)
        answer = response.text
        return answer, None
    except Exception as e:
        return None, str(e)

def test_assistant(name, questions, query_func, *args):
    """Test an assistant with a list of questions"""
    print(f"\n{'='*60}")
    print(f"Testing {name}")
    print(f"{'='*60}")
    
    results = {
        'assistant_name': name,
        'test_time': datetime.now().isoformat(),
        'questions': []
    }
    
    for i, q in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] {q['category']} - Question {q['number']}")
        print(f"Q: {q['question'][:60]}...")
        
        start_time = time.time()
        answer, error = query_func(q['question'], *args)
        elapsed_time = time.time() - start_time
        
        if error:
            print(f"✗ Error: {error}")
            results['questions'].append({
                'question': q['question'],
                'category': q['category'],
                'number': q['number'],
                'answer': None,
                'error': error,
                'time_seconds': elapsed_time,
                'success': False
            })
        else:
            print(f"✓ Response received ({elapsed_time:.1f}s)")
            results['questions'].append({
                'question': q['question'],
                'category': q['category'],
                'number': q['number'],
                'answer': answer,
                'error': None,
                'time_seconds': elapsed_time,
                'success': True
            })
        
        time.sleep(1)  # Rate limiting
    
    return results

def generate_comparison_report(results_customgpt, results_gem):
    """Generate a comparison report"""
    report = []
    report.append("="*80)
    report.append("CUSTOMGPT vs GEM COMPARISON REPORT")
    report.append("="*80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Summary
    report.append("SUMMARY")
    report.append("-"*80)
    
    for results in [results_customgpt, results_gem]:
        if results is None:
            continue
        
        successful = sum(1 for q in results['questions'] if q['success'])
        total_time = sum(q['time_seconds'] for q in results['questions'])
        avg_time = total_time / len(results['questions']) if results['questions'] else 0
        
        report.append(f"\n{results['assistant_name']}:")
        report.append(f"  Successful: {successful}/{len(results['questions'])}")
        report.append(f"  Total time: {total_time:.2f}s")
        report.append(f"  Average time: {avg_time:.2f}s")
    
    # Detailed comparisons
    report.append("\n" + "="*80)
    report.append("DETAILED COMPARISONS")
    report.append("="*80)
    
    if results_customgpt and results_gem:
        for i, (q_cgpt, q_gem) in enumerate(zip(results_customgpt['questions'], results_gem['questions']), 1):
            report.append(f"\n{'='*80}")
            report.append(f"QUESTION {i}: {q_cgpt['category']} - Question {q_cgpt['number']}")
            report.append(f"{'='*80}")
            report.append(f"Question: {q_cgpt['question']}")
            report.append("")
            
            # CustomGPT response
            report.append(f"\nCustomGPT:")
            report.append(f"  Time: {q_cgpt['time_seconds']:.2f}s")
            if q_cgpt['success']:
                answer = q_cgpt['answer']
                if len(answer) > 1000:
                    answer = answer[:1000] + "... [truncated]"
                report.append(f"  Response:\n    {answer.replace(chr(10), chr(10) + '    ')}")
            else:
                report.append(f"  Error: {q_cgpt.get('error', 'Unknown error')}")
            
            # GEM response
            report.append(f"\nGEM:")
            report.append(f"  Time: {q_gem['time_seconds']:.2f}s")
            if q_gem['success']:
                answer = q_gem['answer']
                if len(answer) > 1000:
                    answer = answer[:1000] + "... [truncated]"
                report.append(f"  Response:\n    {answer.replace(chr(10), chr(10) + '    ')}")
            else:
                report.append(f"  Error: {q_gem.get('error', 'Unknown error')}")
            
            report.append("")
    
    return "\n".join(report)

def main():
    """Main function"""
    print("="*80)
    print("STEP 2: ASSISTANT COMPARISON TEST")
    print("="*80)
    print("\nThis script tests CustomGPT and GEM with the same questions.")
    print("Note: API setup required. See README.md for instructions.\n")
    
    # Load questions
    questions = load_test_questions()
    print(f"✓ Loaded {len(questions)} test questions")
    
    # Check for API keys
    print("\nChecking API configuration...")
    
    # For CustomGPT - check OpenAI API key
    customgpt_api_key = None
    if OPENAI_AVAILABLE:
        customgpt_api_key = input("Enter OpenAI API key (for CustomGPT) or press Enter to skip: ").strip()
        if not customgpt_api_key:
            print("⚠ Skipping CustomGPT testing (no API key)")
    
    # For GEM - check Gemini API key
    gem_api_key = None
    if GEMINI_AVAILABLE:
        gem_api_key = input("Enter Google Gemini API key (for GEM) or press Enter to skip: ").strip()
        if not gem_api_key:
            print("⚠ Skipping GEM testing (no API key)")
    
    # Test assistants
    results_customgpt = None
    results_gem = None
    
    if customgpt_api_key:
        print("\nTesting CustomGPT...")
        results_customgpt = test_assistant("CustomGPT", questions, query_customgpt_api, customgpt_api_key)
    
    if gem_api_key:
        print("\nTesting GEM...")
        results_gem = test_assistant("GEM", questions, query_gem_api, gem_api_key)
    
    # Generate report
    if results_customgpt or results_gem:
        print("\n" + "="*80)
        print("GENERATING COMPARISON REPORT")
        print("="*80)
        
        report = generate_comparison_report(results_customgpt, results_gem)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        json_file = OUTPUT_DIR / f"assistant_test_results_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'customgpt': results_customgpt,
                'gem': results_gem
            }, f, indent=2, ensure_ascii=False)
        
        report_file = OUTPUT_DIR / f"comparison_report_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✓ Results saved to: {json_file}")
        print(f"✓ Report saved to: {report_file}")
        print("\n" + report)
    else:
        print("\n⚠ No tests were run. Please configure API keys.")
        print("\nAlternative: Use manual_testing_template.py for manual testing")

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


#!/usr/bin/env python3
"""
Manual Testing Template for Step 2
Use this script to structure your manual testing and generate comparison reports.

This script helps you:
1. Track questions you've asked
2. Record responses from both assistants
3. Generate comparison reports
4. Organize your findings
"""

import json
import time
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "step2_results"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_questions():
    """Load test questions"""
    questions_file = Path(__file__).parent / "test_questions.md"
    questions = []
    
    try:
        with open(questions_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple parsing - look for "**Question**:"
        lines = content.split('\n')
        current_category = None
        
        for i, line in enumerate(lines):
            if line.startswith('## Category'):
                current_category = line.replace('## Category', '').strip()
            elif line.startswith('**Question**:'):
                question_text = line.replace('**Question**:', '').strip()
                # Get question number from previous lines
                q_num = "?"
                for j in range(max(0, i-5), i):
                    if lines[j].startswith('### Question'):
                        q_num = lines[j].replace('### Question', '').strip()
                        break
                
                questions.append({
                    'number': q_num,
                    'category': current_category or 'General',
                    'question': question_text
                })
    except Exception as e:
        print(f"⚠ Could not load questions: {e}")
        questions = [
            {'number': '1', 'category': 'Basic', 'question': 'What is machine learning?'},
            {'number': '2', 'category': 'Company', 'question': 'What services does TechSolutions Inc. offer?'}
        ]
    
    return questions

def manual_test():
    """Interactive manual testing"""
    print("="*80)
    print("STEP 2: MANUAL TESTING TEMPLATE")
    print("="*80)
    print("\nThis script helps you structure manual testing of CustomGPT and GEM.")
    print("You'll be prompted to enter responses after testing each assistant.\n")
    
    questions = load_questions()
    print(f"✓ Loaded {len(questions)} questions\n")
    
    results = {
        'test_time': datetime.now().isoformat(),
        'questions': []
    }
    
    for i, q in enumerate(questions, 1):
        print(f"\n{'='*80}")
        print(f"QUESTION {i}/{len(questions)}")
        print(f"{'='*80}")
        print(f"Category: {q['category']}")
        print(f"Question {q['number']}: {q['question']}")
        print("\n" + "-"*80)
        
        # Get CustomGPT response
        print("\n📝 Testing CustomGPT:")
        print("1. Go to your CustomGPT assistant")
        print(f"2. Ask: {q['question']}")
        print("3. Copy the response below")
        customgpt_response = input("\nCustomGPT Response (or 'skip' to skip): ").strip()
        
        if customgpt_response.lower() == 'skip':
            continue
        
        customgpt_time = input("Response time (seconds, or press Enter): ").strip()
        customgpt_time = float(customgpt_time) if customgpt_time else 0
        
        # Get GEM response
        print("\n📝 Testing GEM:")
        print("1. Go to your GEM assistant")
        print(f"2. Ask: {q['question']}")
        print("3. Copy the response below")
        gem_response = input("\nGEM Response (or 'skip' to skip): ").strip()
        
        if gem_response.lower() == 'skip':
            continue
        
        gem_time = input("Response time (seconds, or press Enter): ").strip()
        gem_time = float(gem_time) if gem_time else 0
        
        # Get comparison notes
        print("\n📊 Comparison:")
        better = input("Which was better? (customgpt/gem/both/skip): ").strip().lower()
        differences = input("Key differences (or press Enter): ").strip()
        
        results['questions'].append({
            'number': q['number'],
            'category': q['category'],
            'question': q['question'],
            'customgpt': {
                'response': customgpt_response,
                'time_seconds': customgpt_time
            },
            'gem': {
                'response': gem_response,
                'time_seconds': gem_time
            },
            'comparison': {
                'better': better,
                'differences': differences
            }
        })
        
        # Ask if continue
        if i < len(questions):
            cont = input(f"\nContinue to next question? (y/n): ").strip().lower()
            if cont != 'y':
                break
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = OUTPUT_DIR / f"manual_test_results_{timestamp}.json"
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Results saved to: {json_file}")
    
    # Generate report
    generate_report(results, timestamp)
    
    return results

def generate_report(results, timestamp):
    """Generate comparison report"""
    report = []
    report.append("="*80)
    report.append("CUSTOMGPT vs GEM - MANUAL TEST COMPARISON")
    report.append("="*80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Summary
    report.append("SUMMARY")
    report.append("-"*80)
    
    customgpt_better = sum(1 for q in results['questions'] if q['comparison']['better'] == 'customgpt')
    gem_better = sum(1 for q in results['questions'] if q['comparison']['better'] == 'gem')
    both_similar = sum(1 for q in results['questions'] if q['comparison']['better'] == 'both')
    
    report.append(f"\nTotal Questions Tested: {len(results['questions'])}")
    report.append(f"CustomGPT Better: {customgpt_better}")
    report.append(f"GEM Better: {gem_better}")
    report.append(f"Both Similar: {both_similar}")
    
    # Detailed comparisons
    report.append("\n" + "="*80)
    report.append("DETAILED COMPARISONS")
    report.append("="*80)
    
    for i, q in enumerate(results['questions'], 1):
        report.append(f"\n{'='*80}")
        report.append(f"QUESTION {i}: {q['category']} - Question {q['number']}")
        report.append(f"{'='*80}")
        report.append(f"Question: {q['question']}")
        report.append("")
        
        # CustomGPT
        report.append(f"\nCustomGPT:")
        report.append(f"  Time: {q['customgpt']['time_seconds']:.2f}s")
        response = q['customgpt']['response']
        if len(response) > 1000:
            response = response[:1000] + "... [truncated]"
        report.append(f"  Response:\n    {response.replace(chr(10), chr(10) + '    ')}")
        
        # GEM
        report.append(f"\nGEM:")
        report.append(f"  Time: {q['gem']['time_seconds']:.2f}s")
        response = q['gem']['response']
        if len(response) > 1000:
            response = response[:1000] + "... [truncated]"
        report.append(f"  Response:\n    {response.replace(chr(10), chr(10) + '    ')}")
        
        # Comparison
        report.append(f"\nComparison:")
        report.append(f"  Better: {q['comparison']['better']}")
        if q['comparison']['differences']:
            report.append(f"  Differences: {q['comparison']['differences']}")
        
        report.append("")
    
    # Save report
    report_file = OUTPUT_DIR / f"manual_comparison_report_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    print(f"✓ Report saved to: {report_file}")
    print("\n" + "\n".join(report))

if __name__ == "__main__":
    try:
        manual_test()
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


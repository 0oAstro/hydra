#!/usr/bin/env python3
"""
Quick test script for the ML Reasoning Pipeline
Tests on 3 samples from training data
"""

import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import pandas as pd
from src import MLReasoningPipeline

def main():
    print("="*80)
    print("ML REASONING PIPELINE - QUICK TEST")
    print("="*80)
    
    # Load training data for testing
    train_file = "ML Challenge Dataset/train.csv"
    train_df = pd.read_csv(train_file)
    
    # Initialize pipeline
    print("\nInitializing pipeline...")
    pipeline = MLReasoningPipeline(train_model=True)
    
    # Test on 3 diverse samples
    print("\n" + "="*80)
    print("TESTING ON 3 SAMPLES")
    print("="*80)
    
    # Get 3 samples from different categories
    test_samples = []
    categories_seen = set()
    
    for idx, row in train_df.iterrows():
        category = row['topic']
        if category not in categories_seen and len(test_samples) < 3:
            test_samples.append(idx)
            categories_seen.add(category)
    
    results = []
    
    for i, sample_idx in enumerate(test_samples):
        sample = train_df.iloc[sample_idx]
        
        print(f"\n{'='*80}")
        print(f"SAMPLE {i+1}/3")
        print(f"{'='*80}")
        
        problem = sample['problem_statement']
        options = {
            'option_1': sample['answer_option_1'],
            'option_2': sample['answer_option_2'],
            'option_3': sample['answer_option_3'],
            'option_4': sample['answer_option_4'],
            'option_5': sample['answer_option_5']
        }
        true_answer = sample['correct_option_number']
        
        print(f"\n📝 Category: {sample['topic']}")
        print(f"❓ Problem: {problem[:150]}...")
        print(f"✅ Correct Answer: Option {true_answer}")
        
        # Process
        result = pipeline.process_problem(problem, options)
        
        predicted = result['predicted_answer']
        confidence = result['confidence']
        
        print(f"\n🤖 Predicted: Option {predicted}")
        print(f"📊 Confidence: {confidence:.1%}")
        print(f"💡 Reasoning: {result['reasoning'][:200]}...")
        
        is_correct = (predicted == true_answer)
        print(f"\n{'✅ CORRECT!' if is_correct else f'❌ WRONG'}")
        
        results.append({
            'sample': i+1,
            'category': sample['topic'],
            'correct': is_correct,
            'confidence': confidence
        })
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    correct_count = sum(1 for r in results if r['correct'])
    accuracy = correct_count / len(results) * 100
    avg_confidence = sum(r['confidence'] for r in results) / len(results)
    
    print(f"\n✅ Accuracy: {accuracy:.1f}% ({correct_count}/{len(results)})")
    print(f"📊 Average Confidence: {avg_confidence:.1%}")
    
    print("\n📋 Per-Sample Results:")
    for r in results:
        status = "✅" if r['correct'] else "❌"
        print(f"  {status} Sample {r['sample']}: {r['category'][:30]:<30} (conf: {r['confidence']:.1%})")
    
    print("\n" + "="*80)
    print("🎉 Test complete!")
    print("="*80)
    
    # Save test results
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n💾 Test results saved to test_results.json")
    
    if accuracy >= 66:  # At least 2/3 correct
        print("\n✅ Pipeline is working correctly!")
        return 0
    else:
        print("\n⚠️ Accuracy lower than expected. Review the results.")
        return 1

if __name__ == "__main__":
    exit(main())


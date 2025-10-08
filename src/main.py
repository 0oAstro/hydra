"""
Main entry point for the ML Reasoning System
Processes test data and generates predictions in JSON format
"""

import json
import sys
import argparse
import pandas as pd
from typing import List, Dict
from tqdm import tqdm

from config import TRAIN_FILE, TEST_FILE, OUTPUT_FILE
from category_classifier import CategoryClassifier
from reasoning_agents import MultiAgentReasoningSystem


class MLReasoningPipeline:
    """Complete ML reasoning pipeline"""
    
    def __init__(self, train_model: bool = True):
        """
        Initialize the pipeline
        
        Args:
            train_model: If True, train category classifier. If False, load existing model.
        """
        print("="*80)
        print("ML REASONING SYSTEM - INITIALIZATION")
        print("="*80)
        
        # Initialize category classifier
        self.category_classifier = CategoryClassifier()
        
        if train_model:
            # Train on training data
            train_df = pd.read_csv(TRAIN_FILE)
            self.category_classifier.train(train_df)
            self.category_classifier.save()
        else:
            # Load existing model
            self.category_classifier.load()
        
        # Initialize reasoning system
        print("\nInitializing reasoning agents...")
        self.reasoning_system = MultiAgentReasoningSystem()
        print("✓ Reasoning agents ready")
        
        print("\n" + "="*80)
        print("SYSTEM READY")
        print("="*80)
    
    def process_problem(self, problem: str, options: Dict[str, str]) -> Dict:
        """
        Process a single problem
        
        Args:
            problem: Problem statement
            options: Dictionary with option_1 through option_5
        
        Returns:
            Dictionary with prediction and reasoning
        """
        # Stage 1: Classify category
        category_result = self.category_classifier.predict(problem, return_probabilities=False)
        predicted_category = category_result['predicted_category']
        category_confidence = category_result['confidence']
        
        # Stage 2: Solve with specialized agent
        solution = self.reasoning_system.solve_problem(
            problem, options, category=predicted_category
        )
        
        # Compile result
        result = {
            'predicted_answer': solution['final_answer'],
            'confidence': solution['confidence'],
            'reasoning': solution['explanation'],
            'category': predicted_category,
            'category_confidence': category_confidence,
            'raw_response': solution.get('raw_response', '')
        }
        
        return result
    
    def process_test_file(self, test_file: str, save_output: bool = True) -> List[Dict]:
        """
        Process entire test file
        
        Args:
            test_file: Path to test CSV file
            save_output: If True, save predictions to output.csv
        
        Returns:
            List of prediction dictionaries
        """
        print(f"\nProcessing test file: {test_file}")
        
        # Load test data
        test_df = pd.read_csv(test_file)
        print(f"Loaded {len(test_df)} test samples")
        
        # Process each sample
        results = []
        predictions_only = []
        
        for idx, row in tqdm(test_df.iterrows(), total=len(test_df), desc="Processing"):
            problem = row['problem_statement']
            options = {
                'option_1': row['answer_option_1'],
                'option_2': row['answer_option_2'],
                'option_3': row['answer_option_3'],
                'option_4': row['answer_option_4'],
                'option_5': row['answer_option_5']
            }
            
            try:
                result = self.process_problem(problem, options)
                result['row_index'] = idx
                results.append(result)
                predictions_only.append(result['predicted_answer'])
            except Exception as e:
                print(f"\nError processing row {idx}: {e}")
                # Default prediction
                results.append({
                    'row_index': idx,
                    'predicted_answer': 3,
                    'confidence': 0.3,
                    'reasoning': f'Error: {str(e)}',
                    'category': 'Unknown',
                    'category_confidence': 0.0,
                    'error': str(e)
                })
                predictions_only.append(3)
        
        # Save output if requested
        if save_output:
            # Save submission file (just predictions)
            output_df = pd.DataFrame({'predicted_answer': predictions_only})
            output_df.to_csv(OUTPUT_FILE, index=False)
            print(f"\n✓ Predictions saved to {OUTPUT_FILE}")
            
            # Save detailed results as JSON
            json_output = OUTPUT_FILE.replace('.csv', '_detailed.json')
            with open(json_output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✓ Detailed results saved to {json_output}")
        
        return results
    
    def process_single_problem(self, problem: str, options: List[str]) -> Dict:
        """
        Process a single problem (for API/interactive use)
        
        Args:
            problem: Problem statement
            options: List of 5 answer options
        
        Returns:
            Dictionary with prediction and reasoning
        """
        if len(options) != 5:
            raise ValueError("Exactly 5 options required")
        
        options_dict = {
            'option_1': options[0],
            'option_2': options[1],
            'option_3': options[2],
            'option_4': options[3],
            'option_5': options[4]
        }
        
        return self.process_problem(problem, options_dict)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='ML Reasoning System')
    parser.add_argument('--test-file', type=str, default=TEST_FILE,
                       help='Path to test CSV file')
    parser.add_argument('--output', type=str, default=OUTPUT_FILE,
                       help='Path to output CSV file')
    parser.add_argument('--no-train', action='store_true',
                       help='Load existing model instead of training')
    parser.add_argument('--single', action='store_true',
                       help='Process a single problem from stdin (JSON format)')
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = MLReasoningPipeline(train_model=not args.no_train)
    
    if args.single:
        # Process single problem from stdin
        print("\nEnter problem data as JSON:")
        print('Format: {"problem": "...", "options": ["opt1", "opt2", "opt3", "opt4", "opt5"]}')
        data = json.loads(sys.stdin.read())
        
        result = pipeline.process_single_problem(
            data['problem'],
            data['options']
        )
        
        # Output as JSON
        print(json.dumps(result, indent=2))
    else:
        # Process test file
        results = pipeline.process_test_file(args.test_file, save_output=True)
        
        # Print summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Total processed: {len(results)}")
        print(f"Average confidence: {sum(r['confidence'] for r in results) / len(results):.1%}")
        
        # Answer distribution
        from collections import Counter
        answer_dist = Counter(r['predicted_answer'] for r in results)
        print("\nAnswer distribution:")
        for answer in sorted(answer_dist.keys()):
            count = answer_dist[answer]
            pct = count / len(results) * 100
            print(f"  Option {answer}: {count:>3} ({pct:>5.1f}%)")
        
        print(f"\n✓ Output saved to {args.output}")


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Simple example showing how to use the ML Reasoning API
"""

import requests
import json

# API endpoint
API_URL = "http://localhost:8000"

def solve_problem(question: str, options: list) -> dict:
    """
    Solve a reasoning problem using the API
    
    Args:
        question: The problem statement
        options: List of 5 answer options
    
    Returns:
        Dictionary with answer and reasoning
    """
    response = requests.post(
        f"{API_URL}/solve",
        json={
            "question": question,
            "options": options
        }
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API error: {response.status_code} - {response.text}")


def main():
    """Example usage"""
    
    # Example 1: Simple math sequence
    print("Example 1: Math Sequence")
    print("-" * 50)
    
    result = solve_problem(
        question="What is the next number in the sequence: 2, 4, 6, 8, ?",
        options=["9", "10", "11", "12", "13"]
    )
    
    print(f"Question: What is the next number in the sequence: 2, 4, 6, 8, ?")
    print(f"Options: 9, 10, 11, 12, 13")
    print(f"\n✓ Answer: Option {result['predicted_answer']} - {result['answer_text']}")
    print(f"✓ Confidence: {result['confidence']:.1%}")
    print(f"✓ Category: {result['category']}")
    print(f"✓ Reasoning: {result['reasoning'][:150]}...")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Logic puzzle
    print("Example 2: Logic Puzzle")
    print("-" * 50)
    
    result = solve_problem(
        question="If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly?",
        options=[
            "Yes, definitely",
            "No, we cannot conclude that",
            "Only in summer",
            "Maybe, depends on the type",
            "Flowers don't fade"
        ]
    )
    
    print(f"Question: If all roses are flowers and some flowers fade quickly,")
    print(f"         can we conclude that some roses fade quickly?")
    print(f"\n✓ Answer: Option {result['predicted_answer']} - {result['answer_text']}")
    print(f"✓ Confidence: {result['confidence']:.1%}")
    print(f"✓ Category: {result['category']}")
    print(f"✓ Reasoning: {result['reasoning'][:200]}...")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Spatial reasoning
    print("Example 3: Spatial Reasoning")
    print("-" * 50)
    
    result = solve_problem(
        question="A cube is painted red on all faces. It is cut into 27 smaller cubes of equal size. How many of the smaller cubes have exactly 2 red faces?",
        options=["6", "8", "12", "16", "24"]
    )
    
    print(f"Question: A cube is painted red on all faces...")
    print(f"\n✓ Answer: Option {result['predicted_answer']} - {result['answer_text']}")
    print(f"✓ Confidence: {result['confidence']:.1%}")
    print(f"✓ Category: {result['category']}")
    print(f"✓ Reasoning: {result['reasoning'][:200]}...")
    
    print("\n" + "="*50)
    print("\n✅ All examples completed!")
    print("\nTo use in your code:")
    print("""
    import requests
    
    result = requests.post(
        'http://localhost:8000/solve',
        json={
            'question': 'Your question here',
            'options': ['opt1', 'opt2', 'opt3', 'opt4', 'opt5']
        }
    ).json()
    
    print(f"Answer: {result['answer_text']}")
    print(f"Reasoning: {result['reasoning']}")
    """)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API server")
        print("\nPlease start the API server first:")
        print("  cd src")
        print("  python api.py")
        print("\nThen run this script again.")
    except Exception as e:
        print(f"❌ Error: {e}")


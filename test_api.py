#!/usr/bin/env python3
"""
Test client for the ML Reasoning API
Demonstrates how to use the REST API
"""

import requests
import json
import time

# API endpoint
API_URL = "http://localhost:8000"


def test_health():
    """Test the health check endpoint"""
    print("="*80)
    print("Testing Health Check")
    print("="*80)
    
    response = requests.get(f"{API_URL}/health")
    
    if response.status_code == 200:
        print("✓ Health check passed")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"✗ Health check failed: {response.status_code}")
    
    print()


def test_single_solve():
    """Test solving a single problem"""
    print("="*80)
    print("Testing Single Problem Solving")
    print("="*80)
    
    # Example problem
    request_data = {
        "question": "What is the next number in the sequence: 2, 4, 6, 8, ?",
        "options": ["9", "10", "11", "12", "13"]
    }
    
    print(f"Question: {request_data['question']}")
    print(f"Options: {request_data['options']}")
    print("\nSending request...")
    
    response = requests.post(
        f"{API_URL}/solve",
        json=request_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\n✓ Success!")
        print(f"\nPredicted Answer: Option {result['predicted_answer']} - {result['answer_text']}")
        print(f"Confidence: {result['confidence']:.1%}")
        print(f"Category: {result['category']}")
        print(f"\nReasoning: {result['reasoning'][:200]}...")
    else:
        print(f"\n✗ Error: {response.status_code}")
        print(response.json())
    
    print()


def test_batch_solve():
    """Test solving multiple problems in batch"""
    print("="*80)
    print("Testing Batch Problem Solving")
    print("="*80)
    
    # Example batch
    batch_data = [
        {
            "question": "What is 2 + 2?",
            "options": ["3", "4", "5", "6", "7"]
        },
        {
            "question": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly?",
            "options": ["Yes", "No", "Cannot be determined", "Only in summer", "Maybe"]
        }
    ]
    
    print(f"Processing {len(batch_data)} problems...")
    
    response = requests.post(
        f"{API_URL}/batch-solve",
        json=batch_data
    )
    
    if response.status_code == 200:
        results = response.json()
        print("\n✓ Success!")
        
        for i, result in enumerate(results):
            print(f"\n--- Problem {i+1} ---")
            print(f"Answer: Option {result['predicted_answer']} - {result['answer_text']}")
            print(f"Confidence: {result['confidence']:.1%}")
            print(f"Category: {result['category']}")
    else:
        print(f"\n✗ Error: {response.status_code}")
        print(response.json())
    
    print()


def test_custom_problem():
    """Test with a custom reasoning problem"""
    print("="*80)
    print("Testing Custom Reasoning Problem")
    print("="*80)
    
    request_data = {
        "question": "A man builds a rectangular house with all four sides facing south. A bear walks by the house. What color is the bear?",
        "options": ["Black", "Brown", "White", "Grey", "Polar bears don't exist"]
    }
    
    print(f"Question: {request_data['question']}")
    print(f"Options: {request_data['options']}")
    print("\nSending request...")
    
    response = requests.post(
        f"{API_URL}/solve",
        json=request_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\n✓ Success!")
        print(f"\nPredicted Answer: Option {result['predicted_answer']} - {result['answer_text']}")
        print(f"Confidence: {result['confidence']:.1%}")
        print(f"Category: {result['category']}")
        print(f"\nReasoning: {result['reasoning']}")
    else:
        print(f"\n✗ Error: {response.status_code}")
        print(response.json())
    
    print()


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("ML REASONING API - CLIENT TEST")
    print("="*80)
    print(f"\nAPI Endpoint: {API_URL}")
    print("Make sure the API server is running!")
    print("Start with: cd src && python api.py")
    print()
    
    # Wait a moment for user to start server if needed
    input("Press Enter when server is ready...")
    
    try:
        # Test health
        test_health()
        
        # Test single solve
        test_single_solve()
        
        # Test batch solve
        test_batch_solve()
        
        # Test custom problem
        test_custom_problem()
        
        print("="*80)
        print("✓ All tests completed!")
        print("="*80)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server")
        print("Make sure the server is running: cd src && python api.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()


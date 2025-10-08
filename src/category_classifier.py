"""
Stage 1: Category Classification
Classifies reasoning problems into categories for specialized agent routing
"""

import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from typing import Dict, Optional
import os

from config import CATEGORY_VECTORIZER_FILE, CATEGORY_CLASSIFIER_FILE, CATEGORY_METADATA_FILE


class CategoryClassifier:
    """Classifies problems into reasoning categories"""
    
    def __init__(self):
        self.vectorizer = None
        self.classifier = None
        self.categories = []
        self.is_trained = False
    
    def train(self, train_df: pd.DataFrame, test_size: float = 0.2):
        """
        Train the category classifier
        
        Args:
            train_df: Training DataFrame with 'problem_statement' and 'topic' columns
            test_size: Fraction of data to use for validation
        """
        print("Training category classifier...")
        
        X = train_df['problem_statement'].values
        y = train_df['topic'].values
        
        # Split for validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Build TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            min_df=2,
            max_df=0.8,
            strip_accents='unicode',
            lowercase=True,
            analyzer='word',
            token_pattern=r'\w{1,}',
            sublinear_tf=True
        )
        
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_val_tfidf = self.vectorizer.transform(X_val)
        
        # Train classifier
        self.classifier = LogisticRegression(
            max_iter=1000,
            C=1.0,
            class_weight='balanced',
            random_state=42,
            solver='lbfgs',
            multi_class='multinomial'
        )
        
        self.classifier.fit(X_train_tfidf, y_train)
        
        # Evaluate
        y_pred = self.classifier.predict(X_val_tfidf)
        accuracy = accuracy_score(y_val, y_pred)
        
        self.categories = self.classifier.classes_.tolist()
        self.is_trained = True
        
        print(f"✓ Category classifier trained with {accuracy:.1%} validation accuracy")
        return accuracy
    
    def predict(self, problem: str, return_probabilities: bool = False) -> Dict:
        """
        Predict the category of a problem
        
        Args:
            problem: Problem statement
            return_probabilities: If True, return all category probabilities
        
        Returns:
            Dictionary with prediction results
        """
        if not self.is_trained:
            raise ValueError("Classifier not trained. Call train() first or load() a trained model.")
        
        problem_tfidf = self.vectorizer.transform([problem])
        prediction = self.classifier.predict(problem_tfidf)[0]
        probabilities = self.classifier.predict_proba(problem_tfidf)[0]
        
        result = {
            'predicted_category': prediction,
            'confidence': max(probabilities)
        }
        
        if return_probabilities:
            category_probs = {
                category: prob 
                for category, prob in zip(self.classifier.classes_, probabilities)
            }
            result['all_probabilities'] = category_probs
        
        return result
    
    def save(self):
        """Save the trained model to disk"""
        if not self.is_trained:
            raise ValueError("Cannot save untrained classifier")
        
        with open(CATEGORY_VECTORIZER_FILE, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        with open(CATEGORY_CLASSIFIER_FILE, 'wb') as f:
            pickle.dump(self.classifier, f)
        
        metadata = {
            'categories': self.categories,
            'num_categories': len(self.categories)
        }
        
        with open(CATEGORY_METADATA_FILE, 'wb') as f:
            pickle.dump(metadata, f)
        
        print(f"✓ Model saved to {os.path.dirname(CATEGORY_CLASSIFIER_FILE)}")
    
    def load(self):
        """Load a trained model from disk"""
        if not os.path.exists(CATEGORY_CLASSIFIER_FILE):
            raise FileNotFoundError(f"Model not found at {CATEGORY_CLASSIFIER_FILE}")
        
        with open(CATEGORY_VECTORIZER_FILE, 'rb') as f:
            self.vectorizer = pickle.load(f)
        
        with open(CATEGORY_CLASSIFIER_FILE, 'rb') as f:
            self.classifier = pickle.load(f)
        
        with open(CATEGORY_METADATA_FILE, 'rb') as f:
            metadata = pickle.load(f)
        
        self.categories = metadata['categories']
        self.is_trained = True
        
        print(f"✓ Model loaded from {os.path.dirname(CATEGORY_CLASSIFIER_FILE)}")
        return self


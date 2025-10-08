"""
ML Reasoning System
A multi-agent reasoning system for solving complex reasoning problems
"""

__version__ = "1.0.0"

from .category_classifier import CategoryClassifier
from .reasoning_agents import MultiAgentReasoningSystem, SpecializedReasoningAgent
from .main import MLReasoningPipeline

# API is optional (requires FastAPI)
try:
    from .api import app as api_app
    __all__ = [
        'CategoryClassifier',
        'MultiAgentReasoningSystem',
        'SpecializedReasoningAgent',
        'MLReasoningPipeline',
        'api_app'
    ]
except ImportError:
    __all__ = [
        'CategoryClassifier',
        'MultiAgentReasoningSystem',
        'SpecializedReasoningAgent',
        'MLReasoningPipeline'
    ]


"""
Configuration settings for the ML Reasoning System
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Model Configuration
GPT_MODEL = "gpt-4-turbo-preview"
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
TEMPERATURE = 0.1  # Low temperature for consistent reasoning

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "ML Challenge Dataset")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
OUTPUT_DIR = DATA_DIR

# Data files
TRAIN_FILE = os.path.join(DATA_DIR, "train.csv")
TEST_FILE = os.path.join(DATA_DIR, "test.csv")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "output.csv")

# Model files
CATEGORY_VECTORIZER_FILE = os.path.join(MODELS_DIR, "category_vectorizer.pkl")
CATEGORY_CLASSIFIER_FILE = os.path.join(MODELS_DIR, "category_classifier.pkl")
CATEGORY_METADATA_FILE = os.path.join(MODELS_DIR, "category_metadata.pkl")

# Processing Configuration
BATCH_SIZE = 10
CHECKPOINT_INTERVAL = 10
MAX_RETRIES = 3

# Ensemble Configuration
ENSEMBLE_METHODS = ['majority_vote', 'confidence_weighted', 'unanimous_only']
DEFAULT_ENSEMBLE_METHOD = 'confidence_weighted'

# Category-specific prompts
CATEGORY_PROMPTS = {
    "Spatial reasoning": """You are an expert in spatial reasoning and 3D visualization.

Problem: {problem}

Answer Options:
1. {option_1}
2. {option_2}
3. {option_3}
4. {option_4}
5. {option_5}

Solve this step-by-step:
1. Identify all spatial elements (shapes, positions, directions, transformations)
2. Visualize the spatial arrangement or movement
3. Track any transformations or changes step by step
4. Calculate the final configuration or answer
5. Check for spatial paradoxes or impossible scenarios
6. Verify your answer against each option

Be careful of:
- Counting errors in 3D structures
- Mirror/rotation confusion
- Hidden surfaces or edges
- Perspective tricks

Provide your reasoning and select the correct option (1-5).
""",

    "Optimization of actions and planning": """You are an expert in optimization, scheduling, and planning.

Problem: {problem}

Answer Options:
1. {option_1}
2. {option_2}
3. {option_3}
4. {option_4}
5. {option_5}

Solve this step-by-step:
1. Identify all tasks, resources, and constraints
2. List all dependencies and time requirements
3. Consider parallel execution possibilities
4. Calculate optimal sequence or allocation
5. Verify the solution meets all constraints
6. Check if this is truly the minimum/maximum

Be careful of:
- Hidden constraints or requirements
- Parallel execution opportunities
- Edge cases and boundary conditions

Provide your reasoning and select the correct option (1-5).
""",

    "Classic riddles": """You are an expert in classic riddles, wordplay, and lateral thinking.

Problem: {problem}

Answer Options:
1. {option_1}
2. {option_2}
3. {option_3}
4. {option_4}
5. {option_5}

Solve this step-by-step:
1. Identify the type of riddle (wordplay, misdirection, literal interpretation)
2. Look for double meanings or unconventional interpretations
3. Consider what assumptions you're making
4. Think about what's NOT being said
5. Look for the "trick" or twist

Provide your reasoning and select the correct option (1-5).
""",

    "Lateral thinking": """You are an expert in lateral thinking puzzles and creative problem solving.

Problem: {problem}

Answer Options:
1. {option_1}
2. {option_2}
3. {option_3}
4. {option_4}
5. {option_5}

Solve this step-by-step:
1. Identify what seems impossible or paradoxical
2. Question ALL assumptions about the scenario
3. Think of unconventional interpretations
4. Consider context that might not be explicitly stated
5. Look for wordplay or alternative meanings

Provide your reasoning and select the correct option (1-5).
""",

    "Sequence solving": """You are an expert in mathematical sequences and pattern recognition.

Problem: {problem}

Answer Options:
1. {option_1}
2. {option_2}
3. {option_3}
4. {option_4}
5. {option_5}

Solve this step-by-step:
1. Write out the sequence clearly
2. Calculate differences between consecutive terms
3. Look for patterns: arithmetic, geometric, polynomial, recursive
4. Check for operations on digits, positions, or values
5. Test your pattern on all given terms

Provide your reasoning and select the correct option (1-5).
""",

    "Operation of mechanisms": """You are an expert in mechanical systems, gears, and machine operations.

Problem: {problem}

Answer Options:
1. {option_1}
2. {option_2}
3. {option_3}
4. {option_4}
5. {option_5}

Solve this step-by-step:
1. Identify all mechanisms, machines, or processes
2. Understand the input/output relationship
3. Calculate rates, ratios, or throughput
4. Consider setup times, cooling periods, or delays
5. Verify the final result mathematically

Provide your reasoning and select the correct option (1-5).
""",

    "Logical traps": """You are an expert in logic puzzles and detecting logical fallacies.

Problem: {problem}

Answer Options:
1. {option_1}
2. {option_2}
3. {option_3}
4. {option_4}
5. {option_5}

Solve this step-by-step:
1. Identify the logical structure and all constraints
2. Look for self-referential or paradoxical statements
3. Check for contradictions in the given information
4. Consider whether the problem itself is the trap
5. Test each option against ALL constraints

Provide your reasoning and select the correct option (1-5).
""",
}

# Create directories if they don't exist
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

